from rest_framework.permissions import IsAuthenticated

from api.management.categories.serializers import CategorySerializer, CategoryProductsSerializer, BulkCategorySerializer
from api.management.views import (
    CreateRestaurantBasedMixin, ListRestaurantBasedMixin, RetrieveRestaurantBasedMixin,
    RetrieveUpdateDeleteRestaurantBasedMixin,
    ListBulkCreateUpdateDestroyRestaurantBasedMixin
)
from api.permissions import RestaurantPermission
from products.models import Category


class CreateListCategoriesView(CreateRestaurantBasedMixin, ListRestaurantBasedMixin):
    """
        Create a Category and List Categories.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['options', 'post', 'get']
    tags = ['categories']


class RetrieveUpdateDeleteCategoryView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
        Retrieve, Update and Delete a Category.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['options', 'get', 'patch', 'delete']
    tags = ['categories']


class ListCategoryProductsView(RetrieveRestaurantBasedMixin):
    """
        Get products by a Category
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = CategoryProductsSerializer
    queryset = Category.objects.all().prefetch_related('products')
    http_method_names = ['options', 'get']
    tags = ['categories']


class BulkUpdateCategoriesView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
    Bulk update categories. Used as drag and drop feature via changing sort_order.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = BulkCategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['options', 'patch']
    tags = ['categories']