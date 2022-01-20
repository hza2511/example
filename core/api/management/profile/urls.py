"""
The urls related to the user profile.

"""
from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path
from api.management.profile.views import (
    CreateTenantUserView, TenantUserView, CreateTenantUserGoogleView,
    CreateTenantUserRestaurantView, UpdateTenantUserRestaurantView,
    ConfirmEmailView, PasswordResetCustomView

)


urlpatterns = [
    # path('signup/', CreateTenantUserView.as_view(), name='create_user'),  # Disabled
    path('me/', TenantUserView.as_view(), name='me'),
    # Google
    path('signup-google/', CreateTenantUserGoogleView.as_view(), name='create_user_google'),
    # Restaurant and user
    path('signup-restaurant/', CreateTenantUserRestaurantView.as_view(), name='create_user_and_restaurant'),
    # Update user and create Restaurant
    path('user-restaurant/', UpdateTenantUserRestaurantView.as_view(), name='update_user_create_restaurant'),
    # Confirm the email
    path('activate/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    # Reset password
    path('password/reset/', PasswordResetCustomView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
