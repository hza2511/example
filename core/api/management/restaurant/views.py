from django_tenants.utils import tenant_context
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status

from api.management.restaurant.serializers import ImageRestaurantSerializer
from api.management.restaurant.serializers import RestaurantSerializer
from api.permissions import RestaurantPermission
from restaurants.models import Restaurant
from restaurants.tasks import celery_provision_tenant


class CreateRestaurantView(CreateAPIView):
    """
        Create a Restaurant
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = RestaurantSerializer
    http_method_names = ['options', 'post']

    def post(self, request, *args, **kwargs):
        serializer: RestaurantSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        celery_provision_tenant.delay(
            host=request.get_host(),
            user_email=request.user.email,
            is_staff=True,
            **serializer.validated_data,
            # image=request.data.get('image'),
            # country=request.data.get('country'),
        )
        return Response(data={"detail": "The creation is in progress."}, status=status.HTTP_201_CREATED)


class ListUpdateDeleteRestaurantView(RetrieveUpdateDestroyAPIView):
    """
        Retrieve, Update and Delete the Restaurant
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all().prefetch_related('domains')
    permission_classes = (IsAuthenticated, RestaurantPermission)
    http_method_names = ['options', 'get', 'patch', 'delete']

    def get(self, request, *args, **kwargs):
        restaurant = self.get_object()
        with tenant_context(restaurant):
            return super(ListUpdateDeleteRestaurantView, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if obj := self.get_object():
            obj.delete(force_drop=True)
            return Response(data={'detail': 'Deleted successfully'})
        return super(ListUpdateDeleteRestaurantView, self).delete(request, *args, **kwargs)


class ImageRestaurantView(UpdateAPIView, DestroyAPIView):
    """
        Upload and Delete the Restaurant image
    """
    queryset = Restaurant.objects.all()
    serializer_class = ImageRestaurantSerializer
    http_method_names = ['options', 'patch', 'delete']
    parser_classes = (FileUploadParser, )
    permission_classes = (IsAuthenticated, RestaurantPermission)

    def patch(self, request, *args, **kwargs):
        restaurant = self.get_object()
        with tenant_context(restaurant):
            return super(ImageRestaurantView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        restaurant = self.get_object()
        with tenant_context(restaurant):
            restaurant.image = None
            restaurant.save()
            return Response(self.get_serializer().to_representation(restaurant), status=status.HTTP_200_OK)
