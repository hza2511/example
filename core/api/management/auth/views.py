from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.views import TokenRefreshView
from api.management.auth.serializers import TokenObtainPairCustomSerializer, TokenObtainPairGoogleSerializer
from rest_framework import serializers
from rest_framework.views import Response, status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class TokenObtainPairCustomView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    Override  TokenObtainPairView to specify custom serializer.
    """
    serializer_class = TokenObtainPairCustomSerializer
    http_method_names = ['options', 'post']
    tags = ['token']

    def post(self, request, *args, **kwargs):
        response = super(TokenObtainPairCustomView, self).post(request, *args, **kwargs)
        response.set_cookie('refresh', response.data.pop('refresh'), httponly=True)
        return response


class TokenObtainPairGoogleView(TokenViewBase):
    """
    Obtain access tokens with google.
    """
    serializer_class = TokenObtainPairGoogleSerializer
    http_method_names = ['options', 'post']
    tags = ['token']

    def post(self, request, *args, **kwargs):
        response = super(TokenObtainPairGoogleView, self).post(request, *args, **kwargs)
        response.set_cookie('refresh', response.data.pop('refresh'), httponly=True)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Transfer refresh token via COOKIES.
    """
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if not (refresh := request.COOKIES.get('refresh')):
            raise serializers.ValidationError({
                "refresh": "Refresh token should be passed in COOKIES."
            })
        data['refresh'] = refresh
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie('refresh', response.data.pop('refresh'), httponly=True)
        return response
