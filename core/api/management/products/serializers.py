from rest_framework import serializers

from api.serializers import BinaryImageSerializer
from products.models import Product,ProductModifiers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from collections import OrderedDict
from typing import List


class ProductModifiersRelationSerializer(serializers.ModelSerializer):
    """
    Serializer for ModifierGroup <--> Product ManyToMany relations.
    """
    def create(self, validated_data: OrderedDict) -> ProductModifiers:
        kwargs = validated_data.copy()
        kwargs.pop('sort_order')
        rel, created = ProductModifiers.objects.update_or_create(
            defaults=validated_data,
            **kwargs
        )
        return rel

    class Meta:
        model = ProductModifiers
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer used to Retrieve and Update a Product. Should not be used to update "image", use
    ImageProductSerializer.

    modifiers:  list of ids. describes relations. All ModifierGroup ids will invoke updating or creating
    corresponding relations. All existed, but not provided, relations will be deleted.
    """
    modifiers = ProductModifiersRelationSerializer(
        many=True,
        required=False,
        write_only=True
    )

    def update(self, instance: Product, validated_data: dict) -> Product:
        modifiers: List[OrderedDict] = validated_data.pop('modifiers')
        super().update(instance, validated_data)
        ProductModifiers.objects.filter(product=instance).exclude(
            modifiers_group__in=[modifier.get('modifiers_group') for modifier in modifiers]
        ).delete()

        for modifier in modifiers:
            modifier['product'] = instance
            ProductModifiersRelationSerializer().create(modifier)
        return instance

    def to_representation(self, instance: Product) -> OrderedDict:
        data = super().to_representation(instance)
        data['modifiers'] = list(x.id for x in instance.modifiers.all())

        return data

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'category', 'sort_order',
                  'modifiers', )
        read_only_fields = ('image', 'id', )


class ImageProductSerializer(BinaryImageSerializer):
    """
        Serializer used to Set and Delete a Product image.
    """

    class Meta:
        model = Product
        fields = ('image', )


class BulkProductSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'category', 'sort_order',)
        read_only_fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'category', )
        list_serializer_class = BulkListSerializer
