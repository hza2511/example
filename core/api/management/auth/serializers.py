from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.management.serializers import GoogleTokenSerializer
from restaurants.models import TenantUser


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):
    """
    Override  TokenObtainPairSerializer to lower() input email for api/token/.
    """
    default_error_messages = {
        'no_active_account': {'detail': ['The username or password you entered is incorrect.']}
    }

    def validate(self, attrs):
        super(TokenObtainPairCustomSerializer, self).validate(attrs)
        attrs['email'] = attrs['email'].lower()
        data = {}
        try:
            user = TenantUser.objects.get(email=attrs['email'])
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)
            return data
        except TenantUser.DoesNotExist:
            pass
        return super(TokenObtainPairCustomSerializer, self).validate(attrs)


class TokenObtainPairGoogleSerializer(GoogleTokenSerializer):
    """
    Obtain access tokens with google.
    """
    google_access_token = serializers.CharField(
        help_text='Google authorization access token.',
        required=True, write_only=True
    )
    email = serializers.CharField(
        help_text="User's email",
        required=True
    )

    def validate(self, attrs):
        data = {}
        attrs['email'] = attrs['email'].lower()
        try:
            user = TenantUser.objects.get(email=attrs['email'])
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            #
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)
            return data
        except TenantUser.DoesNotExist:
            raise serializers.ValidationError('User with that email does not exist.')
