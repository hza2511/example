from rest_framework import serializers

from api.serializers import BinaryImageSerializer
from products.models import Menu
from api.management.categories.serializers import CategorySerializer
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class MenuSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve and Update a Menu. Should not be used to update "image", use
        ImageMenuSerializer.
    """
    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'available', 'created', 'modified', 'image', 'sort_order')
        read_only_fields = ('image', 'id', 'created', 'modified')


class ImageMenuSerializer(BinaryImageSerializer):
    """
        Serializer used to Set and Delete a Menu image.
    """

    class Meta:
        model = Menu
        fields = ('image', )


class MenuCategoriesSerializer(serializers.ModelSerializer):
    """
        Serializer used to List categories by a Menu.
    """
    categories = CategorySerializer(
        help_text='Categories that belong to that Menu',
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Menu
        fields = ('categories', )
        read_only_fields = ('categories', )


class BulkMenuSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'available', 'created', 'modified', 'image', 'sort_order')
        read_only_fields = ('id', 'name', 'description', 'available', 'created', 'modified', 'image',)
        list_serializer_class = BulkListSerializer
