"""
The urls for the Restaurant management
"""
from django.contrib import admin
from django.urls import include
from django.urls import path


urlpatterns = [
    # Auth
    path('', include('api.management.auth.urls')),
    # Profile
    path('', include('api.management.profile.urls')),
    # Restaurant
    path('', include('api.management.restaurant.urls')),
    ### Restaurant based requests ###
    # Menus
    path('restaurant/<int:restaurant_pk>/', include('api.management.menus.urls')),
    # Categories
    path('restaurant/<int:restaurant_pk>/', include('api.management.categories.urls')),
    # Products
    path('restaurant/<int:restaurant_pk>/', include('api.management.products.urls')),
    # Working Schedule
    path('restaurant/<int:restaurant_pk>/', include('api.management.working_schedule.urls')),
    # Venue
    path('restaurant/<int:restaurant_pk>/', include('api.management.venue.urls')),
    # Modifiers
    path('restaurant/<int:restaurant_pk>/', include('api.management.modifiers.urls')),
    #################################
]
