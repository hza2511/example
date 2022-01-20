from rest_framework.permissions import IsAuthenticated

from api.management.modifiers.serializers import (
    ModifiersGroupSerializer, ListModifiersOptionSerializer,
    ModifiersOptionSerializer, ModifiersGroupsSerializer,
    BulkModifiersOptionsSerializer
)
from api.management.views import (
    ListRestaurantBasedMixin, CreateRestaurantBasedMixin, RetrieveUpdateDeleteRestaurantBasedMixin,
    ListBulkCreateUpdateDestroyRestaurantBasedMixin
)
from api.permissions import RestaurantPermission
from products.models import ModifiersGroup, ModifiersOption
from rest_framework import serializers


class ListCreateModifiersGroupsView(ListRestaurantBasedMixin, CreateRestaurantBasedMixin):
    """
        List and Create Modifiers Groups.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ModifiersGroupsSerializer
    queryset = ModifiersGroup.objects.prefetch_related('modifiers__modifiers__options').all()
    http_method_names = ['options', 'get', 'post']
    tags = ['modifiers']


class RetrieveUpdateModifiersGroupView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
    Retrieve, Update and Delete a Modifiers Group.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ModifiersGroupSerializer
    queryset = ModifiersGroup.objects.prefetch_related('modifiers__modifiers__options').all()
    http_method_names = ['options', 'get', 'delete', 'put']
    tags = ['modifiers']


class ListCreateUpdateModifiersOptionView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
        Bulk List, Create and Update Modifiers Options.
        Warning: use POST for both: POST (create) and PATCH (partial update). Objects with "id" field would be updated.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ListModifiersOptionSerializer
    queryset = ModifiersOption.objects.all()
    http_method_names = ['options', 'get', 'post']
    tags = ['modifiers']

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if not isinstance(data, list):
            raise serializers.ValidationError({'details': 'Incorrect input. Required: [{}, {}]'})
        to_create = list(filter(lambda row: not row.get('id'), data))
        to_update = list(filter(lambda row: row.get('id'), data))
        # CREATE
        request.data.clear()
        request.data.extend(to_create)
        super(ListCreateUpdateModifiersOptionView, self).post(request, *args, **kwargs)
        # UPDATE
        request.data.clear()
        request.data.extend(to_update)
        super(ListCreateUpdateModifiersOptionView, self).patch(request, *args, **kwargs)
        # Todo: list only received objects
        return super(ListCreateUpdateModifiersOptionView, self).get(request, *args, **kwargs)


class DeleteModifiersOptionsView(RetrieveUpdateDeleteRestaurantBasedMixin):
    """
    Delete a Modifiers Option.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = ModifiersOptionSerializer
    queryset = ModifiersOption.objects.all()
    http_method_names = ['options', 'delete']
    tags = ['modifiers']


class BulkUpdateModifiersOptionsView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
    Bulk update modifiers options. Used as drag and drop feature via changing sort_order.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = BulkModifiersOptionsSerializer
    queryset = ModifiersOption.objects.all()
    http_method_names = ['options', 'patch']
    tags = ['modifiers']

