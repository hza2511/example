"""
The urls related to the restaurant creation, updating.

"""
from django.urls import path
from api.management.restaurant.views import CreateRestaurantView, ListUpdateDeleteRestaurantView, ImageRestaurantView

urlpatterns = [
    # path('restaurant/', CreateRestaurantView.as_view(), name='create_restaurant'),    # Disabled
    path('restaurant/<int:pk>/', ListUpdateDeleteRestaurantView.as_view(), name='get_update_restaurant'),
    path('restaurant/<int:pk>/image/', ImageRestaurantView.as_view(), name='upload_delete_restaurant_image'),
]
