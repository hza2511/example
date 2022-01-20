from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.management.profile.serializers import (
    TenantUserSerializer, CreateTenantUserSerializer,
    CreateTenantUserGoogleSerializer, TenantUserRestaurantSerializer,
    UpdateUserRestaurantSerializer, ConfirmEmailSerializer,
    PasswordResetCustomSerializer
)
from rest_framework.views import Response, status
from dj_rest_auth.views import PasswordResetView


class CreateTenantUserView(CreateAPIView):
    """
        Create an user
    """
    serializer_class = CreateTenantUserSerializer
    http_method_names = ['options', 'post']
    tags = ['signup']


class TenantUserView(RetrieveAPIView):
    """
    Get an user object
    """
    serializer_class = TenantUserSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['options', 'get']
    tags = ['signup']

    def get_object(self):
        return self.request.user


class CreateTenantUserGoogleView(CreateAPIView):
    """
        Create an user with google
    """
    serializer_class = CreateTenantUserGoogleSerializer
    http_method_names = ['options', 'post']
    tags = ['signup']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # refresh token via cookies
        data = serializer.data.copy()
        refresh_token = data.pop('refresh')
        headers = self.get_success_headers(data)
        response = Response(data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie('refresh', refresh_token, httponly=True)
        return response


class CreateTenantUserRestaurantView(CreateAPIView):
    """
    Create an user and a restaurant.
    """
    serializer_class = TenantUserRestaurantSerializer
    http_method_names = ['options', 'post']
    tags = ['signup']

    def get_serializer_context(self):
        ctx = super(CreateTenantUserRestaurantView, self).get_serializer_context()
        ctx.update({
            'host': self.request.get_host()
        })
        return ctx


class UpdateTenantUserRestaurantView(CreateAPIView):
    """
    Set user's phone number and create a restaurant.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserRestaurantSerializer
    http_method_names = ['options', 'post']
    tags = ['signup']

    def get_serializer_context(self):
        ctx = super(UpdateTenantUserRestaurantView, self).get_serializer_context()
        ctx.update({
            'host': self.request.get_host(),
            "user": self.request.user
        })
        return ctx


class ConfirmEmailView(CreateAPIView):
    """
    Confirm a user's email and activate the user's profile.
    """
    serializer_class = ConfirmEmailSerializer
    http_method_names = ['options', 'post']
    tags = ['profile']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=kwargs)
        serializer.is_valid(raise_exception=True)
        # refresh token via cookies.
        data = serializer.data.copy()
        refresh = data.pop('refresh')
        response = Response(data=data, status=status.HTTP_200_OK)
        response.set_cookie('refresh', refresh, httponly=True)
        return response


class PasswordResetCustomView(PasswordResetView):
    """
    Request resetting user's password. An email is send in the background.
    """
    serializer_class = PasswordResetCustomSerializer
    http_method_names = ['options', 'post']
    tags = ['profile']
