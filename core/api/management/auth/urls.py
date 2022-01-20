"""
The urls related to the authentication.

"""
from django.urls import path
from api.management.auth.views import TokenObtainPairCustomView, TokenObtainPairGoogleView, CustomTokenRefreshView

urlpatterns = [
    # JWT token
    path('token/', TokenObtainPairCustomView.as_view(), name='get_token_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # Google
    path('token-google/', TokenObtainPairGoogleView.as_view(), name='token_obtain_pair_google'),
]
