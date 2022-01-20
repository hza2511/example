from rest_framework import serializers

from products.models import Category
from api.management.products.serializers import ProductSerializer
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class CategorySerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve and Update a Category. Should not be used to update "image", use
        ImageCategorySerializer.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'menu', 'available', "sort_order")
        read_only_fields = ('id', )


class CategoryProductsSerializer(serializers.ModelSerializer):
    """
        Serializer used to List products by a Category.
    """
    products = ProductSerializer(
        help_text='Products that belong to that Category',
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Category
        fields = ('products', )
        read_only_fields = ('products', )


class BulkCategorySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'menu', 'available', 'sort_order')
        read_only_fields = ('id', 'name', 'description', 'menu', 'available', )
        list_serializer_class = BulkListSerializer
