from rest_framework.permissions import IsAuthenticated

from api.management.venue.serializers import (
    AreaSerializer, TableSerializer, AreaTablesSerializer
)
from api.management.views import (
    ListRestaurantBasedMixin, CreateRestaurantBasedMixin, RetrieveUpdateDeleteRestaurantBasedMixin,
    RetrieveRestaurantBasedMixin,
)
from api.permissions import RestaurantPermission
from restaurant_info.models import Area, Table
from restaurants.models import Domain
from django.db.models import Count


class ListCreateAreaView(ListRestaurantBasedMixin, CreateRestaurantBasedMixin):
    """
        List and Create areas.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = AreaSerializer
    queryset = Area.objects.all().annotate(tables_amount=Count('tables')).prefetch_related('tables')
    http_method_names = ['options', 'get', 'post']
    tags = ['venue']


class RetrieveUpdateDeleteAreaView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
        Retrieve, Update and Delete an area.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = AreaSerializer
    queryset = Area.objects.all().annotate(tables_amount=Count('tables'))
    http_method_names = ['options', 'get', 'patch', 'delete']
    tags = ['venue']


class ListCreateTableView(ListRestaurantBasedMixin, CreateRestaurantBasedMixin):
    """
        List and Create tables.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    http_method_names = ['options', 'get', 'post']
    tags = ['venue']

    def get_serializer_context(self, **kwargs):
        ctx = super(ListCreateTableView, self).get_serializer_context()

        ctx.update({
            'domain': Domain.objects.filter(
               tenant_id=self.kwargs.get('restaurant_pk')
            ).first(),
            'protocol': self.request._request.scheme
        })

        return ctx


class RetrieveUpdateDeleteTableView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
        Retrieve, Update and Delete a table.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = TableSerializer
    queryset = Table.objects.all().prefetch_related('area')
    http_method_names = ['options', 'get', 'patch', 'delete']
    tags = ['venue']

    def get_serializer_context(self, **kwargs):
        ctx = super(RetrieveUpdateDeleteTableView, self).get_serializer_context()

        ctx.update({
            'domain': Domain.objects.filter(
                tenant_id=self.kwargs.get('restaurant_pk')
            ).first(),
            'protocol': self.request._request.scheme
        })

        return ctx


class ListAreaTablesView(RetrieveRestaurantBasedMixin):
    """
        Get tables in an area.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = AreaTablesSerializer
    queryset = Area.objects.all().prefetch_related('tables')
    http_method_names = ['options', 'get']
    tags = ['venue']
