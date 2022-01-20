from django.db.models import Q
from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from restaurant_info.models import WorkingDay, WorkingHours
from datetime import datetime


# class WorkingDaySerializer(serializers.ModelSerializer):
#     """
#         Serializer used to Retrieve and Update a WorkingDay.
#     """
#
#     class Meta:
#         model = WorkingDay
#         fields = ('id', 'name', 'weekday', 'open_24', 'closed')
#         read_only_fields = ('id', 'name', 'weekday',)
#
#     def validate(self, attrs):
#         open_24 = attrs.get('open_24')
#         closed = attrs.get('closed')
#         if open_24 and closed:
#             raise serializers.ValidationError({
#                 'open_24': 'The restaurant can not be opened and closed at the same time',
#                 'closed': 'The restaurant can not be opened and closed at the same time'
#             })
#
#         if open_24 and self.instance.closed:
#             self.instance.closed = False
#             self.instance.save()
#         elif closed and self.instance.open_24:
#             self.instance.open_24 = False
#             self.instance.save()
#         return attrs


class WorkingHoursSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve, Create and Update WorkingHours.
    """

    class Meta:
        model = WorkingHours
        fields = ('id', 'opens', 'closes', 'working_day')
        read_only_fields = ('id',)

    def validate(self, attrs):
        opens = attrs.get('opens') or self.instance.opens
        closes = attrs.get('closes') or self.instance.closes
        working_day = attrs.get('working_day') or self.instance.working_day

        if closes and opens:
            if closes <= opens:
                raise serializers.ValidationError({
                    'closes': 'The restaurant can not close before it has opened.'
                })

        # validate with existing
        if WorkingHours.objects.filter(
                Q(opens__lte=closes) & Q(closes__gte=opens),
                working_day=working_day
        ).exists():
            raise serializers.ValidationError({
                'opens': 'Working hours can not overlap.',
                'closes': 'Working hours can not overlap.'
            })
        return attrs


# class WorkingDayWorkingHoursSerializer(serializers.ModelSerializer):
#     """
#         Serializer used to List WorkingHours by a WorkingDay.
#     """
#     working_hours = WorkingHoursSerializer(
#         help_text='WorkingHours during that WorkingDay',
#         many=True, read_only=True, required=False
#     )
#
#     class Meta:
#         model = WorkingDay
#         fields = ('working_hours',)
#         read_only_fields = ('working_hours',)


class BulkWorkingDaysSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    working_hours = WorkingHoursSerializer(
        help_text='Working hours of that day.',
        many=True, required=False, read_only=True
    )

    class Meta:
        model = WorkingDay
        fields = ('id', 'name', 'weekday', 'open_24', 'closed', 'working_hours')
        read_only_fields = ('id', 'name', 'weekday', 'working_hours')
        list_serializer_class = BulkListSerializer


class BulkWorkingHoursSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    Serializer used to Retrieve, Create and Update WorkingHours.
    """
    id = serializers.IntegerField(
        help_text='id of the working hour. Needed to update an existing object.',
        required=False,
    )

    def validate(self, attrs):
        opens = attrs.get('opens') or self.instance.opens
        closes = attrs.get('closes') or self.instance.closes
        working_day = attrs.get('working_day') or self.instance.working_day
        instance_id = attrs.get('id')

        # Check valid id given
        if instance_id:
            if not WorkingHours.objects.filter(id=instance_id).exists():
                raise serializers.ValidationError({
                    "id": f"Object with id {instance_id} does not exist."
                })

        if closes and opens:
            if closes < opens or opens == closes:
                raise serializers.ValidationError({
                    'closes': 'The restaurant can not close before it has opened.'
                })

        all_data = self.initial_data

        # Check duplicates
        try:
            duplicates = len(list(filter(
                lambda x:
                datetime.strptime(
                    x.get('opens'), '%H:%M' if len(x.get('opens')) == 5 else '%H:%M:%S'
                ).time() == opens and
                datetime.strptime(
                    x.get('closes'), '%H:%M' if len(x.get('closes')) == 5 else '%H:%M:%S'
                ).time() == closes and x.get('working_day') == working_day.id, all_data))
            )
            overlap = len(list(filter(
                lambda x:
                datetime.strptime(
                    x.get('opens'), '%H:%M' if len(x.get('opens')) == 5 else '%H:%M:%S'
                ).time() <= closes and
                datetime.strptime(
                    x.get('closes'), '%H:%M' if len(x.get('closes')) == 5 else '%H:%M:%S'
                ).time() >= opens and x.get('working_day') == working_day.id, all_data))
            )
        except Exception as e:
            raise serializers.ValidationError({
                "details": f"Inappropriate input. {e}. Expected formats: 10:20 or 10:20:05",
            })
        if duplicates > 1:  # > 1 because we also get the current values
            raise serializers.ValidationError({
                'details': 'Duplicates found.',
                'opens': opens,
                'closes': closes
            })
        # Check overlap
        if overlap > 1:     # > 1 because we also get the current values
            raise serializers.ValidationError({
                'opens': 'Working hours can not overlap.',
                'closes': 'Working hours can not overlap.'
            })

        # validate with existing
        if WorkingHours.objects.filter(
                Q(opens__lte=closes) & Q(closes__gte=opens),
                working_day=working_day
        ).exclude(id__in=[x.get('id') for x in all_data]).exists():
            raise serializers.ValidationError({
                'opens': 'Working hours can not overlap.',
                'closes': 'Working hours can not overlap.'
            })
        return attrs

    class Meta:
        model = WorkingHours
        fields = ('id', 'opens', 'closes', 'working_day')
        list_serializer_class = BulkListSerializer
