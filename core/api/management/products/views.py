from rest_framework.permissions import IsAuthenticated

from api.management.products.serializers import ProductSerializer, ImageProductSerializer, BulkProductSerializer
from api.management.views import (
    CreateRestaurantBasedMixin, ListRestaurantBasedMixin, RetrieveUpdateRestaurantBasedMixin, SetDeleteBinaryImageView,
    RetrieveUpdateDeleteRestaurantBasedMixin, ListBulkCreateUpdateDestroyRestaurantBasedMixin
)
from api.permissions import RestaurantPermission
from products.models import Product, ModifiersGroup
from django.db.models import Prefetch


class CreateListProductsView(CreateRestaurantBasedMixin, ListRestaurantBasedMixin):
    """
        Create a Product and List Products.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['options', 'post', 'get']
    tags = ['products']


class RetrieveUpdateDeleteProductView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
        Retrieve, Update and Delete a Product.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ProductSerializer
    queryset = Product.objects.all().prefetch_related(Prefetch('modifiers', queryset=ModifiersGroup.objects.all().order_by('productmodifiers__sort_order')))
    http_method_names = ['options', 'get', 'patch', 'delete']
    tags = ['products']


class ImageProductView(SetDeleteBinaryImageView):
    """
        Upload and Delete the Product image
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ImageProductSerializer
    queryset = Product.objects.all()
    tags = ['products']


class BulkUpdateProductsView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
    Bulk update products. Used as drag and drop feature via changing sort_order.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = BulkProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['options', 'patch']
    tags = ['products']
