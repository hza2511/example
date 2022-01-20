import copy

from django.conf import settings
from django_tenants.utils import parse_tenant_config_path
from drf_yasg.generators import OpenAPISchemaGenerator
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class TenantsS3Boto3Storage(S3Boto3Storage):
    """
    Implementation that extends S3Boto3Storage for multi-tenant setups.
    File path customized setting.
    """
    @property
    def location(self):
        _location = parse_tenant_config_path(
            "%s%s" % (settings.AWS_LOCATION, settings.MULTITENANT_RELATIVE_MEDIA_ROOT))
        # Put here extra path. storage_path/{extra_path}/path/to/file
        return _location


class CustomS3StaticStorage(S3StaticStorage):
    @property
    def location(self):
        _location = settings.AWS_LOCATION_STATIC
        return _location


class CustomSchemaGenerator(OpenAPISchemaGenerator):

    def get_overrides(self, view, method):
        """Get overrides specified for a given operation.

        :param view: the view associated with the operation
        :param str method: HTTP method
        :return: a dictionary containing any overrides set by :func:`@swagger_auto_schema <.swagger_auto_schema>`
        :rtype: dict
        """
        method = method.lower()
        action = getattr(view, 'action', method)
        action_method = getattr(view, action, None)
        overrides = getattr(action_method, '_swagger_auto_schema', {})
        if method in overrides:
            overrides = overrides[method]
        tags = getattr(view, 'tags', None)
        if tags:
            overrides['tags'] = tags

        return copy.deepcopy(overrides)
