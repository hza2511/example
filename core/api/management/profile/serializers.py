from django.contrib.auth import password_validation
from django.contrib.auth.models import update_last_login
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.serializers import PasswordResetSerializer
from api.management.auth.serializers import TokenObtainPairCustomSerializer
from api.management.restaurant.serializers import RestaurantSerializer
from api.management.serializers import GoogleTokenSerializer
from restaurants.models import TenantUser
from restaurants.tasks import celery_provision_tenant, send_verification_mail
from django.utils.encoding import force_text
from api.views import TokenGenerator
from django.utils.http import urlsafe_base64_decode
from restaurants.tasks import send_reset_email
from django.contrib.sites.shortcuts import get_current_site


class TenantUserSerializer(serializers.ModelSerializer):
    """
        TenantUser (user) serializer. Use to retrieve the TenantUser object.
    """
    restaurants = RestaurantSerializer(many=True, source='tenants')

    def validate_email(self, email):
        email = email.lower()
        return email

    class Meta:
        model = TenantUser
        fields = ('id', 'email', 'full_name', 'phone_number', 'restaurants')


class CreateTenantUserSerializer(TenantUserSerializer):
    """
        TenantUser (user) serializer. Use to create the TenantUser object.
        Representation data is extended with authentication credentials (JWT tokens).
    """

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def save(self, **kwargs):
        user = super(CreateTenantUserSerializer, self).save(**kwargs)
        user.set_password(self.validated_data.get('password'))
        user.save()
        return user

    def to_representation(self, instance):
        data = super(CreateTenantUserSerializer, self).to_representation(instance)
        token_serializer = TokenObtainPairCustomSerializer(data=self.validated_data)
        token_serializer.is_valid(raise_exception=True)
        data.update(token_serializer.validated_data)
        return data

    class Meta:
        model = TenantUser
        fields = ('id', 'email', 'full_name', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CreateTenantUserGoogleSerializer(serializers.ModelSerializer, GoogleTokenSerializer):
    google_access_token = serializers.CharField(
        help_text='Google authorization access token.',
        required=True, write_only=True
    )
    full_name = serializers.CharField(
        help_text="User's full_name. Retrieved from google.",
        required=False
    )
    # email = serializers.EmailField(validators=[
    #     UniqueValidator(
    #         queryset=TenantUser.objects.all(),
    #         message="Email is already used",
    #     ), EmailValidator]
    # )
    # Todo: customize message for email validation?

    def validate(self, attrs):
        try:
            google_response = attrs.pop('google_access_token')
        except KeyError:
            raise serializers.ValidationError({
                "google_access_token": "Something went wrong with google validation."
            })
        attrs['full_name'] = google_response.get('name')
        # attrs['is_google'] = True # TODO: if there will be a need to mark google users.
        return attrs

    def to_representation(self, instance):
        data = super(CreateTenantUserGoogleSerializer, self).to_representation(instance)
        refresh = RefreshToken.for_user(self.instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.instance)
        return data

    class Meta:
        model = TenantUser
        fields = ('email', 'full_name', 'google_access_token')
        read_only_fields = ('google_access_token', )


class TenantUserRestaurantSerializer(GoogleTokenSerializer, serializers.Serializer):
    """
    Serializer to create an user and a restaurant at one moment.
    """
    email = serializers.EmailField(
        help_text="User's email.",
        validators=[UniqueValidator(
            queryset=TenantUser.objects.all(),
            message="Email is already used",
        ), EmailValidator]
    )
    full_name = serializers.CharField(
        help_text="User's full name.",
        max_length=128
    )
    password = serializers.CharField(
        help_text="User's password",
        max_length=128,
        required=True, write_only=True,
    )
    # google_access_token = serializers.CharField(
    #     help_text='Google authorization access token.',
    #     required=False, write_only=True,
    # )
    phone_number = serializers.CharField(
        help_text="User's phone number.",
        max_length=20,
        validators=[UniqueValidator(
            queryset=TenantUser.objects.all(),
            message="Phone number is already used",
        ), ]
    )
    business_name = serializers.CharField(
        help_text='The business (restaurant) name.',
        max_length=64
    )

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     # google_access_token = attrs.get('google_access_token')
    #     if not any((password, google_access_token)):
    #         raise serializers.ValidationError({
    #             "details": "No valid credentials found.",
    #             "password": "Password is required to sign up if not google_access_token is provided.",
    #             "google_access_token": "Google access token is required to sign up with google."
    #         })
    #     return attrs

    def to_representation(self, instance):
        data = {}
        data['restaurant'] = 'Creation is in progress.'
        return data

    def create(self, validated_data):
        user = TenantUser(
            email=validated_data.get('email'),
            full_name=validated_data.get('full_name'),
            phone_number=validated_data.get('phone_number'),
        )
        user.save()
        if validated_data.get('password'):  # Todo: no "if" if password required
            user.set_password(validated_data.get('password'))
            user.save()

        celery_provision_tenant.delay(
            host=self.context.get('host'),
            user_email=user.email,
            name=validated_data.get('business_name'),
            is_staff=True,
        )
        send_verification_mail.delay(
            email=user.email,
            host=self.context.get('host'),
            is_secure=self.context.get('request').is_secure(),
        )

        return user

    def update(self, instance, validated_data):
        pass


# TODO: move  google_access_token field to GoogleTokenSerializer?


class UpdateUserRestaurantSerializer(GoogleTokenSerializer, serializers.Serializer):
    """
    Serializer to update user's phone_nu,ber and a restaurant at one moment.
    """
    phone_number = serializers.CharField(
        help_text="User's phone number.",
        max_length=20,
        validators=[UniqueValidator(
            queryset=TenantUser.objects.all(),
            message="Phone number is already used",
        ), ]
    )
    business_name = serializers.CharField(
        help_text='The business (restaurant) name.',
        max_length=64
    )

    def create(self, validated_data):
        user = self.context.get('user')
        user.phone_number = validated_data.get('phone_number')
        user.save()

        celery_provision_tenant.delay(
            host=self.context.get('host'),
            user_email=user.email,
            name=validated_data.get('business_name'),
            is_staff=True,
        )

        return user

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        user = self.context.get('user')
        exceptions = {}
        if user.phone_number:
            exceptions['user'] = 'This user already has a phone number.'
        if user.tenants.exists():
            exceptions['restaurant'] = 'This user has already created a restaurant.'
        if exceptions:
            raise serializers.ValidationError(exceptions)

        return attrs

    def to_representation(self, instance):
        data = {}
        data['restaurant'] = 'Creation is in progress.'
        return data


class ConfirmEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(
        help_text='uuid',
        required=True
    )
    token = serializers.CharField(
        help_text='token',
        required=True
    )

    def validate(self, attrs):
        account_activation_token = TokenGenerator()
        try:
            uid = force_text(urlsafe_base64_decode(attrs.get('uidb64')))
            user = TenantUser.objects.get(id=uid)
            self.instance = user
        except(TypeError, ValueError, OverflowError, TenantUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, attrs.get('token')):
            user.is_active = True
            user.save()
        else:
            raise serializers.ValidationError({
                "details": 'Activation link is invalid!'
            })

        return attrs

    def to_representation(self, instance):
        data = {}
        refresh = RefreshToken.for_user(self.instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.instance)

        return data


class PasswordResetCustomSerializer(PasswordResetSerializer):
    """
    Customized serializer for resetting password.
    """

    def validate_email(self, email):
        if not TenantUser.objects.filter(email=email):
            raise serializers.ValidationError("We could not find any user with that email.")
        super(PasswordResetCustomSerializer, self).validate_email(email)

    def get_email_options(self):
        return {
            'subject_template_name': 'password_reset/password_reset_email_subject.html',
            'html_email_template_name': 'password_reset/password_reset_body_email.html',
        }

    def save(self):
        ctx = self.context
        r = ctx.pop('request')
        ctx['is_secure'] = r.is_secure()
        ctx.pop('view')
        domain_override = get_current_site(r).domain
        send_reset_email.delay(
            context=ctx, email_options=self.get_email_options(),
            initial_data=self.initial_data, domain_override=domain_override,
        )
