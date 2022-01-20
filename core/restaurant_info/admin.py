
from django.contrib import admin

from restaurant_info.models import Area, Table, WorkingDay, WorkingHours


# Register your models here.
class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 0
    fields = ('opens', 'closes', )


class TableInline(admin.TabularInline):
    model = Table
    extra = 0
    fields = ('name', )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    inlines = (TableInline, )


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'area')

    # Todo: implement form for creation as in serializer
    def has_add_permission(self, request):
        return False


@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ('name', 'weekday', 'open_24', 'closed')
    readonly_fields = ('name', 'weekday')
    inlines = (WorkingHoursInline, )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'opens', 'closes', 'working_day')
