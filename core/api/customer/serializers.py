"""
    subdomain
"""

from django.utils import timezone
from django_tenants.utils import tenant_context
from rest_framework import serializers

from products.models import Product, ModifiersGroup, Menu, Category, ModifiersOption
from restaurant_info.models import WorkingDay, WorkingHours, Table
from restaurants.models import Restaurant
from restaurants.serializers import DomainSerializer


class RestaurantInfoSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve RestaurantInfo.
    """
    domains = DomainSerializer(many=True, read_only=True, required=False)
    is_working = serializers.BooleanField(
        help_text='Is restaurant working right now (according to working hours).',
        read_only=True
    )

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'description', 'email', 'phone_number', 'website', 'street', 'building', 'country',
                  'city', 'postal_code', 'image', 'domains', 'ordering_instructions', 'no_available_menus',
                  'allow_mobile_ordering', 'allow_live_payments', 'is_working')
        read_only_fields = ('image', 'id', 'domains', 'is_working')

    def to_representation(self, instance: Restaurant):
        data = super(RestaurantInfoSerializer, self).to_representation(instance)
        with tenant_context(instance):
            now = timezone.now()
            working_day: WorkingDay = WorkingDay.objects.prefetch_related('working_hours').get(weekday=now.isoweekday())
            if working_day.open_24:
                is_working = True
            elif working_day.closed:
                is_working = False
            else:
                is_working = WorkingHours.objects.filter(
                    opens__lte=now, closes__gte=now,
                    working_day=working_day
                ).exists()
        data['is_working'] = is_working
        return data


class ModifiersOptionSerializer(serializers.ModelSerializer):
    """
        Serializer used to Retrieve a ModifiersOption.
    """
    class Meta:
        model = ModifiersOption
        fields = ('id', 'name', 'price', 'in_stock', 'group', 'sort_order')
        read_only_fields = ('id', 'name', 'price', 'in_stock', 'group', 'sort_order')


class ModifiersSerializer(serializers.ModelSerializer):
    """
    ModifierGroup with Options
    """
    options = ModifiersOptionSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = ModifiersGroup
        fields = ('id', 'name', 'description', 'min_options', 'max_options', 'options')
        read_only_fields = ('id', 'name', 'description', 'min_options', 'max_options', 'options')


class ProductsSerializer(serializers.ModelSerializer):
    """
    Serializer used to Get products.
    """
    modifiers = ModifiersSerializer(many=True, required=False, read_only=True)

    def to_representation(self, instance):
        data = super(ProductsSerializer, self).to_representation(instance)
        return data

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'category', 'sort_order',
                  'modifiers')
        read_only_fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'category',
                            'sort_order', 'modifiers')


class ProductsNestedSerializer(serializers.ModelSerializer):
    """
    Serializer used to Get products.
    """
    modifiers = ModifiersSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'sort_order',
                  'modifiers')
        read_only_fields = ('id', 'name', 'description', 'available', 'image', 'popular', 'price', 'sort_order',
                            'modifiers')


class CategoryNestedSerializer(serializers.ModelSerializer):
    """
    Serializer to get categories with all nested relations.
    """
    products = ProductsNestedSerializer(
        help_text='Products that belong to that Category',
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'available', 'products', )
        read_only_fields = ('id', 'name', 'description', 'available', 'products', )


class WholeMenuSerializer(serializers.ModelSerializer):
    """
    Serializer represents the whole Menu data.
    """
    categories = CategoryNestedSerializer(
        help_text='Categories that belong to that menu',
        many=True, required=False,
        read_only=True
    )

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'available', 'created', 'modified', 'image', 'categories', 'sort_order')
        read_only_fields = ('id', 'name', 'description', 'available', 'created', 'modified', 'image', 'categories')


class TableSerializer(serializers.ModelSerializer):
    """
    Serializer represents a Table objects.
    """
    class Meta:
        model = Table
        fields = ('id', 'name', )
        read_only_fields = ('id', 'name', )
