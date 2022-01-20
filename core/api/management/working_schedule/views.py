from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from api.management.views import (
    # ListRestaurantBasedMixin, RetrieveUpdateRestaurantBasedMixin,
    # CreateRestaurantBasedMixin,
    RetrieveUpdateDeleteRestaurantBasedMixin,
    # RetrieveRestaurantBasedMixin,
    ListBulkCreateUpdateDestroyRestaurantBasedMixin
)
from api.management.working_schedule.serializers import (
    # WorkingDaySerializer,
    WorkingHoursSerializer,
    # WorkingDayWorkingHoursSerializer,
    BulkWorkingDaysSerializer, BulkWorkingHoursSerializer
)
from api.permissions import RestaurantPermission
from restaurant_info.models import WorkingDay, WorkingHours


# class ListWorkingDayView(ListRestaurantBasedMixin):
#     """
#         List working days.
#     """
#     permission_classes = (IsAuthenticated, RestaurantPermission)
#     serializer_class = WorkingDaySerializer
#     queryset = WorkingDay.objects.all()
#     http_method_names = ['options', 'get']
#     tags = ['working_schedule']


class BulkListWorkingDayView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
    List and bulk Update working days.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = BulkWorkingDaysSerializer
    queryset = WorkingDay.objects.all().prefetch_related('working_hours')
    http_method_names = ['options', 'get', 'patch']
    tags = ['working_schedule']


# class RetrieveUpdateWorkingDayView(RetrieveUpdateRestaurantBasedMixin):
#     """
#         Retrieve and Update a working day.
#     """
#     permission_classes = (IsAuthenticated, RestaurantPermission)
#     serializer_class = WorkingDaySerializer
#     queryset = WorkingDay.objects.all()
#     http_method_names = ['options', 'get', 'patch']
#     tags = ['working_schedule']


# class CreateListWorkingHoursView(CreateRestaurantBasedMixin, ListRestaurantBasedMixin):
#     """
#         Create and List working hours.
#     """
#     permission_classes = (IsAuthenticated, RestaurantPermission)
#     serializer_class = WorkingHoursSerializer
#     queryset = WorkingHours.objects.all()
#     http_method_names = ['options', 'post', 'get', 'patch']
#     tags = ['working_schedule']


class BulkCreateListWorkingHoursView(ListBulkCreateUpdateDestroyRestaurantBasedMixin):
    """
    Bulk Create, Update and List working hours. Warning: use POST for both: POST (create) and PATCH (partial update).
    Objects with "id" field would be updated.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = BulkWorkingHoursSerializer
    queryset = WorkingHours.objects.all()
    http_method_names = ['options', 'post', 'get', ]
    tags = ['working_schedule']

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if not isinstance(data, list):
            raise serializers.ValidationError({'details': 'Incorrect input. Required: [{}, {}]'})
        to_create = list(filter(lambda row: not row.get('id'), data))
        to_update = list(filter(lambda row: row.get('id'), data))
        # CREATE
        request.data.clear()
        request.data.extend(to_create)
        super(BulkCreateListWorkingHoursView, self).post(request, *args, **kwargs)
        # UPDATE
        request.data.clear()
        request.data.extend(to_update)
        super(BulkCreateListWorkingHoursView, self).patch(request, *args, **kwargs)

        return super(BulkCreateListWorkingHoursView, self).get(request, *args, **kwargs)


class RetrieveUpdateDeleteWorkingHoursView(RetrieveUpdateDeleteRestaurantBasedMixin):
    # """
    #     Retrieve, Update and Delete a working hours.
    # """
    """
    Delete a working hour.
    """
    permission_classes = (IsAuthenticated, RestaurantPermission)
    serializer_class = WorkingHoursSerializer
    queryset = WorkingHours.objects.all()
    # http_method_names = ['options', 'get', 'patch', 'delete']
    http_method_names = ['options', 'delete']
    tags = ['working_schedule']


# class ListWorkingDayWorkingHoursView(RetrieveRestaurantBasedMixin):
#     """
#         Get working hours by a working day
#     """
#     permission_classes = (IsAuthenticated, RestaurantPermission)
#     serializer_class = WorkingDayWorkingHoursSerializer
#     queryset = WorkingDay.objects.all().prefetch_related('working_hours')
#     http_method_names = ['options', 'get']
#     tags = ['working_schedule']
