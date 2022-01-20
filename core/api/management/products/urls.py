from django.urls import path

from api.management.products.views import (
    CreateListProductsView, RetrieveUpdateDeleteProductView, ImageProductView,
    BulkUpdateProductsView
)

urlpatterns = [
    path('products/', CreateListProductsView.as_view(), name='create_list_products'),
    path('products/<int:pk>/', RetrieveUpdateDeleteProductView.as_view(), name='retrieve_update_product'),
    path('products/<int:pk>/image/', ImageProductView.as_view(), name='set_delete_product_image'),
    path('products_bulk/', BulkUpdateProductsView.as_view(), name='bulk_update_products'),
]
