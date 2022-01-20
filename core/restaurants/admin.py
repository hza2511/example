from django.contrib import admin
from restaurants.models import Restaurant, TenantUser, Domain
from django.utils.html import format_html
from django.db.models import Prefetch
from django.apps import apps
from django_tenants.utils import get_public_schema_name


# Register your models here.
class TenantsAdmin(admin.ModelAdmin):
    """
    Hides public models from tenants
    """
    def has_view_permission(self, request, view=None, **kwargs):
        if request.tenant.schema_name == get_public_schema_name():
            return super().has_view_permission(request, view)
        else:
            return False

    def has_add_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return super().has_add_permission(request)
        else:
            return False

    def has_change_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return super().has_change_permission(request, view)
        else:
            return False

    def has_delete_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return super().has_delete_permission(request, view)
        else:
            return False

    def has_view_or_change_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return super().has_view_or_change_permission(request, view)
        else:
            return False


# app = apps.get_app_config('restaurants')
# override_admin_models = ('restaurant', 'domain', 'restaurantowner')
# for model_name, model in app.models.items():
#     if model_name not in override_admin_models:
#         admin.site.register(model, TenantsAdmin)


###
@admin.register(Restaurant)
class RestaurantAdmin(TenantsAdmin):
    def get_queryset(self, request):
        queryset = super(RestaurantAdmin, self).get_queryset(request).prefetch_related(
            Prefetch('domains',))# queryset=Domain.objects.only('domain')))
        return queryset

    def image_url(self, obj: Restaurant):
        url = obj.image.url.replace('/public/', '/%s/' % obj.schema_name)
        return format_html('<a href="%s" target="_blank">%s</a>' % (url, url))

    def get_domain(self, obj: Restaurant):
        domain = obj.domains.first()
        if domain:
            domain = domain.domain

        return format_html('<a href="//%s" target="_blank">%s</a>' % (domain, domain))

    get_domain.short_description = 'domain'

    list_display = ('name', 'email', 'country', 'get_domain')
    readonly_fields = ('is_created', 'image_url', 'get_domain')
    exclude = ('schema_name', 'slug', 'image')

    actions = None


@admin.register(TenantUser)
class TenantUserAdmin(TenantsAdmin):
    readonly_fields = ('tenants', "is_active", "is_verified", )
    exclude = ('password', )

    actions = None

