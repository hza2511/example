"""
Only management related base views.
"""
from restaurants.models import Restaurant
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
)
from django_tenants.utils import tenant_context
from rest_framework.views import Response, status
from django_tenants.utils import tenant_context
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView


class RestaurantBasedMixin:
    """
        Base class for Restaurant based request.
        api/restaurant/<restaurant_pk>/
    """
    def get_restaurant(self, restaurant_pk, obj=None):
        return get_object_or_404(Restaurant, pk=restaurant_pk)


class SetDeleteBinaryImageView(UpdateAPIView, DestroyAPIView, RestaurantBasedMixin):
    """
        Base class for Restaurant based requests for uploading image binary (base64)
    """
    parser_classes = (FileUploadParser, )
    http_method_names = ['options', 'patch', 'delete']

    def patch(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk'),
        )
        with tenant_context(restaurant):
            return super(SetDeleteBinaryImageView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk'),
        )
        obj = self.get_object()
        with tenant_context(restaurant):
            obj.image = None
            obj.save()
            return Response(self.get_serializer().to_representation(restaurant), status=status.HTTP_200_OK)


class CreateRestaurantBasedMixin(CreateAPIView, RestaurantBasedMixin):
    """
        Base class for POST Restaurant based requests.
    """
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(CreateRestaurantBasedMixin, self).post(request, *args, **kwargs)


class ListRestaurantBasedMixin(ListAPIView, RestaurantBasedMixin):
    """
        Base class for POST Restaurant based requests.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(ListRestaurantBasedMixin, self).get(request, *args, **kwargs)


class RetrieveRestaurantBasedMixin(RetrieveAPIView, RestaurantBasedMixin):
    """
        Base class for GET a single object based on the Restaurant requests.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveRestaurantBasedMixin, self).get(request, *args, **kwargs)


class RetrieveUpdateRestaurantBasedMixin(RetrieveUpdateAPIView, RestaurantBasedMixin):
    """
        Base class for GET and PATCH a single object based on the Restaurant requests.
    """
    # TODO: remove just RETRIEVE? and limit in http_method_names?
    http_method_names = ['get', 'patch']

    def get(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveUpdateRestaurantBasedMixin, self).get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveUpdateRestaurantBasedMixin, self).patch(request, *args, **kwargs)


class RetrieveUpdateDeleteRestaurantBasedMixin(RetrieveUpdateDestroyAPIView, RestaurantBasedMixin):
    """
        Base class for GET, PATCH and DELETE a single object based on the Restaurant requests.
    """
    http_method_names = ['get', 'patch', 'delete']

    def get(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveUpdateDeleteRestaurantBasedMixin, self).get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveUpdateDeleteRestaurantBasedMixin, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveUpdateDeleteRestaurantBasedMixin, self).delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return super(RetrieveUpdateDeleteRestaurantBasedMixin, self).put(request, *args, **kwargs)

# TODO: Create base classes for every type. Create MIXINs.


class ListBulkCreateUpdateDestroyRestaurantBasedMixin(ListBulkCreateUpdateDestroyAPIView, RestaurantBasedMixin):
    """
        Base class for Bulk GET, POST, PUT, PATCH and DELETE based on the Restaurant requests.
    """
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return self.bulk_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return self.partial_bulk_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        restaurant = self.get_restaurant(
            restaurant_pk=kwargs.get('restaurant_pk')
        )
        with tenant_context(restaurant):
            return self.bulk_destroy(request, *args, **kwargs)

    def bulk_destroy(self, request, *args, **kwargs):
        qs = self.get_queryset()

        filtered = qs.filter(id__in=[obj.get('id') for obj in request.data])

        if not self.allow_bulk_destroy(qs, filtered):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_bulk_destroy(filtered)

        return Response(status=status.HTTP_204_NO_CONTENT)
