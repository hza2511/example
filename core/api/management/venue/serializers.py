from rest_framework import serializers

from restaurant_info.models import Area, Table

from collections import OrderedDict


class TableSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve and Update a Table.
    """

    class Meta:
        model = Table
        fields = ('id', 'name', 'area',)     # 'uuid', 'link', 'file',
        read_only_fields = ('id', )   # 'uuid', 'link', 'file',

    def to_representation(self, instance):
        data = super(TableSerializer, self).to_representation(instance)
        if (
                (domain := self.context.get('domain')) is not None
        ) and (
                (protocol := self.context.get('protocol')) is not None
        ):
            table_name = "-".join(instance.name.lower().split())
            area_name = "-".join(instance.area.name.lower().split())
            table_param = f'{area_name}-table-{table_name}'
            data['link'] = f'{protocol}://{domain}/?tableId={table_param}'
        return data

    def validate_name(self, name: str) -> str:
        if '-' in name:
            raise serializers.ValidationError('"-" is disallowed in the table name.')
        return name

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        attrs.setdefault('id', self.instance.id if self.instance is not None else None)
        attrs.setdefault('area', self.instance.area if self.instance is not None else None)
        area = attrs.get('area')
        if Table.objects.filter(name__iexact=attrs.get('name'), area=area).exclude(pk=attrs.get('id')).exists():
            raise serializers.ValidationError({
                "name": "Table names should be case insensitively unique."
            })
        return attrs
    # def validate(self, attrs):
    #     # domain = self.context.get('domain')
    #     # scheme = self.context.get('scheme')
    #
    #     # Prevent changing on update request
    #     if not self.instance:
    #         # Validate uuid with db
    #         for _ in range(20):
    #             table_uuid = uuid.uuid4()
    #             if not Table.objects.filter(uuid=table_uuid).exists():
    #                 attrs['uuid'] = table_uuid
    #                 # attrs['link'] = f'{domain}?tableId={table_uuid}'
    #                 break
    #         else:
    #             if not attrs.get('uuid'):
    #                 raise serializers.ValidationError({
    #                     "uuid": "Could not find available uuid. Try again."
    #                 })
    #     self.is_valid()
    #     return attrs


class AreaSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve and Update an Area.
    """
    tables_amount = serializers.IntegerField(
        required=False, read_only=True
    )

    class Meta:
        model = Area
        fields = ('id', 'name', 'tables_amount',)
        read_only_fields = ('id', 'tables_amount',)

    def validate_name(self, name: str) -> str:
        if '-' in name:
            raise serializers.ValidationError('"-" is disallowed in the area name.')
        return name


class AreaTablesSerializer(serializers.ModelSerializer):
    """
        Serializer used to List Tables in an Area.
    """
    tables = TableSerializer(
        help_text='Tables located in that Area',
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Area
        fields = ('tables', )
        read_only_fields = ('tables', )
