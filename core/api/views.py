"""
Base views.
"""
# from django_tenants.utils import tenant_context
# from rest_framework.generics import UpdateAPIView, DestroyAPIView
# from rest_framework.parsers import FileUploadParser
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import Response, status


import six
# class SetDeleteBinaryImageView(UpdateAPIView, DestroyAPIView):
#     """
#         Base class for uploading image binary (base64)
#     """
#     # move to api.management.viewes?
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (FileUploadParser, )
#     http_method_names = ['options', 'patch', 'delete']
#
#     def patch(self, request, *args, **kwargs):
#         restaurant = self.get_object()
#         with tenant_context(restaurant):
#             return super(SetDeleteBinaryImageView, self).patch(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         restaurant = self.get_object()
#         with tenant_context(restaurant):
#             restaurant.image = None
#             restaurant.save()
#             return Response(self.get_serializer().to_representation(restaurant), status=status.HTTP_200_OK)
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )
