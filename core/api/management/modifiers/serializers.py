from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from products.models import ModifiersGroup, ModifiersOption
from typing import OrderedDict


class ModifiersOptionSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve and Update a ModifiersOption.
    """
    class Meta:
        model = ModifiersOption
        fields = ('id', 'group', 'name', 'price', 'in_stock', 'sort_order')
        read_only_fields = ('id', )
        list_serializer_class = BulkListSerializer


class ModifiersGroupsSerializer(serializers.ModelSerializer):
    """
    Serializer used to Retrieve and Update a ModifiersGroup.
    """
    min_options = serializers.IntegerField(
        help_text='The minimum amount of the options can be chosen.',
        min_value=0, max_value=10,
        required=True,
    )
    max_options = serializers.IntegerField(
        help_text='The maximum amount of the options can be chosen.',
        min_value=0, max_value=10,
        required=True,
    )
    options = ModifiersOptionSerializer(
        help_text='Options related to that group.',
        many=True, required=False, read_only=True
    )

    class Meta:
        model = ModifiersGroup
        fields = ('id', 'name', 'description', 'min_options', 'max_options', 'options')
        read_only_fields = ('id', 'options')

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if attrs.get('max_options') < attrs.get('min_options'):
            raise serializers.ValidationError({
                'max_options': "The maximum amount of the options can not be less than minimum."
            })
        return attrs


class ModifiersGroupSerializer(ModifiersGroupsSerializer):
    """
    Serializer used to Retrieve and Update a ModifiersGroup.
    """
    options = ModifiersOptionSerializer(
        help_text='Options related to that group.',
        many=True, required=False, read_only=True
    )

    class Meta:
        model = ModifiersGroup
        fields = ('id', 'name', 'description', 'min_options', 'max_options', 'options',)
        read_only_fields = ('id', 'options')

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        attrs = super(ModifiersGroupSerializer, self).validate(attrs)
        total_options: int = self.instance.options.count()
        errors = {}
        max_options: int = attrs.get('max_options')
        min_options: int = attrs.get('min_options')
        if max_options > total_options:
            errors['max_options'] = "The maximum amount of the options can not be more then total amount of options. " \
                                    "Add Some options firstly."
        if min_options > total_options:
            errors['min_options'] = "The minimum amount of the options can not be more then total amount of options. " \
                                    "Add Some options firstly."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class ListModifiersOptionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    Serializer used to Retrieve, Create and Update a List of ModifiersOptions.
    """
    # Todo: check the amount of options for the group and minimum?
    id = serializers.IntegerField(
        help_text='id of the modifiers option. Needed to update an existing object.',
        required=False,
    )

    def validate(self, attrs):
        # Check unique name in the group
        obj_id = attrs.get('id')
        if not obj_id or not isinstance(obj_id, int):
            obj_id = None
        if ModifiersOption.objects.filter(
                group=attrs.get('group'), name=attrs.get('name')
        ).exclude(id=obj_id).exists():
            raise serializers.ValidationError({
                "name": "Option with such a name already exists in that group.",
                "group": "Option with such a name already exists in that group."
            })

        # Validate with initial data
        all_data = self.initial_data
        duplicates = len(list(filter(
            lambda x: x.get('group') == attrs.get('group').id and x.get('name') == attrs.get('name'),
            all_data
        )))
        if duplicates > 1:
            raise serializers.ValidationError({
                'details': 'Duplicates found.',
                'group': attrs.get('group').id,
                'name': attrs.get('name')
            })
        return attrs

    class Meta:
        model = ModifiersOption
        fields = ('id', 'group', 'name', 'price', 'in_stock', 'sort_order')
        read_only_fields = ('id',)
        list_serializer_class = BulkListSerializer


class BulkModifiersOptionsSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ModifiersOption
        fields = ('id', 'group', 'name', 'price', 'in_stock', 'sort_order')
        read_only_fields = ('id', 'group', 'name', 'price', 'in_stock', )
        list_serializer_class = BulkListSerializer
