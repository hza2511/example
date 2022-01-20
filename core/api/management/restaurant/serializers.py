from rest_framework import serializers

from api.serializers import BinaryImageSerializer
from restaurants.models import Restaurant
from api.serializers import DomainSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve and Update a Restaurant. Should not be used to update "image", use
        ImageRestaurantSerializer.
    """
    domains = DomainSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'description', 'email', 'phone_number', 'website', 'street', 'building', 'country',
                  'city', 'postal_code', 'image', 'domains', 'ordering_instructions', 'no_available_menus',
                  'allow_mobile_ordering', 'allow_live_payments')
        read_only_fields = ('image', 'id', 'domains', )


class ImageRestaurantSerializer(BinaryImageSerializer):
    """
        Serializer used to Set and Delete a Restaurant image.
    """

    class Meta:
        model = Restaurant
        fields = ('image', )
