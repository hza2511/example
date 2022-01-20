from django.urls import path

from api.management.categories.views import (
    CreateListCategoriesView, RetrieveUpdateDeleteCategoryView, ListCategoryProductsView,
    BulkUpdateCategoriesView
)

urlpatterns = [
    path('categories/', CreateListCategoriesView.as_view(), name='create_list_categories'),
    path('categories/<int:pk>/', RetrieveUpdateDeleteCategoryView.as_view(), name='retrieve_update_category'),
    path('categories/<int:pk>/products/', ListCategoryProductsView.as_view(), name='list_category_products'),
    path('categories_bulk/', BulkUpdateCategoriesView.as_view(), name='bulk_update_categories'),
]
