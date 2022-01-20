from rest_framework.permissions import IsAuthenticated

from api.management.menus.serializers import (
    MenuSerializer, ImageMenuSerializer, MenuCategoriesSerializer,
    BulkMenuSerializer
)
from api.management.views import (
    CreateRestaurantBasedMixin, ListRestaurantBasedMixin, SetDeleteBinaryImageView,
    RetrieveRestaurantBasedMixin, RetrieveUpdateDeleteRestaurantBasedMixin,
    ListBulkCreateUpdateDestroyRestaurantBasedMixin
)
from api.permissions import RestaurantPermission
from products.models import Menu


class CreateListMenusView(CreateRestaurantBasedMixin, ListRestaurantBasedMixin):
    """
        Create a Menu and List Menus.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    http_method_names = ['options', 'post', 'get']
    tags = ['menus']


class RetrieveUpdateDeleteMenuView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
        Retrieve, Update and Delete a Menu.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    http_method_names = ['options', 'get', 'patch', 'delete']
    tags = ['menus']


class ImageMenuView(SetDeleteBinaryImageView):
    """
        Upload and Delete the Menu image
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ImageMenuSerializer
    queryset = Menu.objects.all()
    http_method_names = ['options', 'patch', 'delete']
    tags = ['menus']


class ListMenuCategoriesView(RetrieveRestaurantBasedMixin):
    """
        Get categories by a Menu
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = MenuCategoriesSerializer
    queryset = Menu.objects.all().prefetch_related('categories')
    http_method_names = ['options', 'get']
    tags = ['menus']


class BulkUpdateMenusView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
    Bulk update menus. Used as drag and drop feature via changing sort_order.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = BulkMenuSerializer
    queryset = Menu.objects.all()
    http_method_names = ['options', 'patch']
    tags = ['menus']
