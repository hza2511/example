from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.customer.serializers import (
    ProductsSerializer, WholeMenuSerializer, RestaurantInfoSerializer,
    TableSerializer,
 # AllNestedDataSerializer,
)
from api.management.categories.serializers import CategorySerializer
from api.management.menus.serializers import MenuSerializer
from products.models import Menu, Category, Product
from restaurant_info.models import Table


class InfoView(RetrieveAPIView):
    """
        Restaurant info view
    """
    serializer_class = RestaurantInfoSerializer
    http_method_names = ['get', 'options']

    def get_object(self):
        return self.request.tenant


class MenusView(ListAPIView):
    """
        Restaurant menus view
    """
    serializer_class = MenuSerializer
    queryset = Menu.available_menus()
    # queryset = Menu.objects.all()[:1]
    http_method_names = ['get', 'options']


class CategoriesView(ListAPIView):
    """
        Restaurant Categories view
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['get', 'options']


class ProductsView(ListAPIView):
    """
        Restaurant products view
    """
    serializer_class = ProductsSerializer
    queryset = Product.objects.prefetch_related('modifiers', 'modifiers__options').all()
    http_method_names = ['get', 'options']


class TableView(RetrieveAPIView):
    """
    Retrieve a Table by its id.
    """
    serializer_class = TableSerializer
    http_method_names = ['options', 'get']

    def get_object(self):
        area_name, table_name = tuple(map(
            lambda x: x.replace('-', ' '),  # format as needed.
            self.kwargs.get('area_table').split('-table-')  # parse area name and table name.
        ))
        return Table.objects.filter(name__iexact=table_name, area__name__iexact=area_name).first()


class WholeMenuView(RetrieveAPIView):
    """
    Get whole Menu data.
    """
    serializer_class = WholeMenuSerializer
    queryset = Menu.filled_menus()
    http_method_names = ['get', 'options']
