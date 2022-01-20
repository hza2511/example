"""URL Configuration
The urls for the non subdomains.
Examples:
    domain.com/
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
    path('api/', include('api.general.urls')),  # non Restaurant related urls
    path('api/', include('api.management.urls')),  # Restaurant management urls
]

if settings.DEBUG:
    SchemaViewPublic = get_schema_view(
        openapi.Info(
            title="Public API.",
            default_version='v1',
            description="not yet =(",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=urlpatterns,
        generator_class=CustomSchemaGenerator,
    )

    urlpatterns += [
        # Swagger
        path('api/swagger/', SchemaViewPublic.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-public'),
        path('api/docs/', SchemaViewPublic.with_ui('redoc', cache_timeout=0), name='schema-redoc-public'),
    ]
