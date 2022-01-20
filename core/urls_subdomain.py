"""URL Configuration
The urls for the subdomains.
Examples:
    subdomain.domain.com/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from settings.utils import CustomSchemaGenerator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.customer.urls')),
]


if settings.DEBUG:
    SchemaViewTenant = get_schema_view(
        openapi.Info(
            title="Tenant related API.",
            default_version='v1',
            description="not yet =(",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=urlpatterns,
        generator_class=CustomSchemaGenerator
    )

    urlpatterns += [
        # Swagger
        path('api/swagger/', SchemaViewTenant.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-tenant'),
        path('api/docs/', SchemaViewTenant.with_ui('redoc', cache_timeout=0), name='schema-redoc-tenant'),
    ]
