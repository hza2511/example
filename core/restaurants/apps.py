from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'

    def ready(self):
        from django.conf import settings
        from django.core.management import call_command
        from django.db import connections
        from django_tenants.models import schema_exists
        from django_tenants.postgresql_backend.base import _check_schema_name
        from django_tenants.utils import get_tenant_database_alias
        if not schema_exists(settings.TENANT_BASE_SCHEMA):
            # safety check
            connection = connections[get_tenant_database_alias()]
            _check_schema_name(settings.TENANT_BASE_SCHEMA)
            cursor = connection.cursor()
            # Create Schema
            cursor.execute('CREATE SCHEMA "%s"' % settings.TENANT_BASE_SCHEMA)
            call_command('migrate_schemas',
                         tenant=True,
                         schema_name=settings.TENANT_BASE_SCHEMA,
                         interactive=False,
                         verbosity=1)

            connection.set_schema_to_public()
