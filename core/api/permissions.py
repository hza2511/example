from rest_framework import permissions
from restaurants.models import Restaurant


class RestaurantPermission(permissions.BasePermission):
    """
    Global permission check for user having access to the Restaurant.
    """
    message = 'You have no access to that restaurant.'

    def get_requested_restaurant(self, request):
        kwargs = request.parser_context.get('kwargs')

        if restaurant_pk := kwargs.get('restaurant_pk'):
            try:
                restaurant = Restaurant.objects.get(pk=restaurant_pk)
                return restaurant
            except Restaurant.DoesNotExist:
                return

    def has_object_permission(self, request, view, obj):
        # Refactor if permissions should be granted based on the tenant permissions
        if not isinstance(obj, Restaurant):
            obj = self.get_requested_restaurant(request)

        return request.user == obj.owner

    def has_permission(self, request, view):
        restaurant = self.get_requested_restaurant(request)
        if restaurant:
            return self.has_object_permission(request, view, obj=restaurant)

        return super(RestaurantPermission, self).has_permission(request, view)

