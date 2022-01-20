"""
All the urls for subdomains.
"""
from django.urls import path
from api.customer.views import (
    InfoView, MenusView, CategoriesView,
    ProductsView, WholeMenuView, TableView
)

urlpatterns = [
    path('info/', InfoView.as_view(), name='restaurant_info'),
    path('menus/', MenusView.as_view(), name='menus'),
    path('menus/<int:pk>/', WholeMenuView.as_view(), name='whole_menu'),
    path('table/<str:area_table>/', TableView.as_view(), name='table'),
    # path('categories/', CategoriesView.as_view(), name='categories'),
    path('products/', ProductsView.as_view(), name='products'),
]
