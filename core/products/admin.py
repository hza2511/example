from django.contrib import admin
from django.utils.html import format_html

from products.models import Menu, Category, Product, ModifiersOption, ModifiersGroup


# Register your models here.
class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    fields = ('name', 'description', 'available')


# class ProductInline(admin.TabularInline):
#     model = Product
#     extra = 0
#     fields = ('name', 'description', 'price', 'category', 'popular', 'available', 'modifiers', 'sort_order')


class ModifiersOptionInline(admin.TabularInline):
    model = ModifiersOption
    extra = 0
    fields = ('name', 'price', 'in_stock', 'sort_order')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    def image_path(self, obj: Menu):
        return format_html('<a href="%s" target="_blank">%s</a>' % (obj.image.url, obj.image.name))

    image_path.short_description = 'Image'

    list_display = ('name', 'available', 'created', 'modified')
    readonly_fields = ('created', 'image_path')
    exclude = ('image', )
    inlines = (CategoryInline, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('menu', 'name', 'available')
    list_display_links = ('name', )
    # inlines = (ProductInline, )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_path(self, obj: Product):
        return format_html('<a href="%s" target="_blank">%s</a>' % (obj.image.url, obj.image.name))

    image_path.short_description = 'Image'

    list_display = ('name', 'popular', 'available', 'category')
    readonly_fields = ('image_path', )
    exclude = ('image', )


@admin.register(ModifiersGroup)
class ModifiersGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_options', 'max_options')
    inlines = (ModifiersOptionInline, )


@admin.register(ModifiersOption)
class ModifiersOptionAdmin(admin.ModelAdmin):
    list_display = ('group', 'name', 'price', 'in_stock')
