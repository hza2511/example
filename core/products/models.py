from django.db import models
import time
from sort_order_field import SortOrderField
from django.db.models import Count, Prefetch, Q


def menu_image_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "menus/%s_%i.%s" % (instance, (int(time.time())), extension)

    return new_filename.lower()


def product_image_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "products/%s_%i.%s" % (instance, (int(time.time())), extension)

    return new_filename.lower()


# Create your models here.
class Menu(models.Model):
    name = models.CharField(
        help_text='The name of the menu',
        max_length=32
    )
    description = models.TextField(
        help_text='The description of the menu',
        max_length=512,
        null=True, blank=True
    )
    available = models.BooleanField(
        help_text='The status of the menu. Enabled / Disabled',
        default=False
    )
    created = models.DateTimeField(
        help_text='When was the menu created',
        auto_created=True,
        auto_now=True,
        blank=True, null=True
    )
    modified = models.DateTimeField(
        help_text='When was the menu modified last time',
        auto_now=True,
        blank=True, null=True
    )
    image = models.ImageField(
        help_text='The image of the menu',
        blank=True, null=True,
        upload_to=menu_image_dir_path
    )
    sort_order = SortOrderField(
        help_text='The order of the menu',
    )

    def __str__(self):
        return self.name

    @classmethod
    def available_menus(cls):
        return cls.objects.filter(
            available=True,
        ).annotate(
            products_count=Count('categories__products', filter=Q(categories__products__available=True))
                   ).filter(products_count__gt=0).order_by('sort_order')

    @classmethod
    def filled_menus(cls):
        """
        Filter categories for Menu, so that each one has at least one available Product.
        :return: Menu
        """
        return cls.objects.prefetch_related(Prefetch('categories', queryset=Category.objects.annotate(
            products_count=Count('products')).prefetch_related('products').filter(products_count__gt=0).order_by("sort_order")
        ), 'categories__products', 'categories__products')

    class Meta:
        ordering = ['-available', 'sort_order']


class Category(models.Model):
    menu = models.ForeignKey(
        help_text='The Menu this category belongs to',
        to='products.Menu',
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(
        help_text='The name of the category',
        max_length=32
    )
    description = models.TextField(
        help_text='The description of the category',
        max_length=512,
        null=True, blank=True
    )
    available = models.BooleanField(
        help_text='The status of the category. Enabled / Disabled',
        default=False
    )
    sort_order = SortOrderField(
        help_text='The order of the category in the menu',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order']


class Product(models.Model):
    name = models.CharField(
        help_text='The name of the product',
        max_length=32
    )
    description = models.TextField(
        help_text='The description of the product',
        max_length=512,
        null=True, blank=True
    )
    image = models.ImageField(
        help_text='The image of the product',
        blank=True, null=True,
        upload_to=product_image_dir_path
    )
    popular = models.BooleanField(
        help_text='Is that product popular?',
        default=False
    )
    available = models.BooleanField(
        help_text='The status of the product. Enabled / Disabled',
        default=False
    )
    price = models.DecimalField(
        help_text='The price of the product',
        max_digits=9, decimal_places=2,
    )
    category = models.ForeignKey(
        help_text='The Category that product belongs to',
        to='products.Category',
        on_delete=models.CASCADE,
        related_name='products',
    )
    sort_order = SortOrderField(
        help_text='The order of the product in the menu',
    )
    modifiers = models.ManyToManyField(
        help_text='Possible Modifiers for that product',
        through='products.ProductModifiers',
        to='products.ModifiersGroup',
        blank=True,
        related_name='modifiers',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order']


class ModifiersGroup(models.Model):
    name = models.CharField(
        help_text='The name of the Modifiers Group',
        max_length=32
    )
    description = models.TextField(
        help_text='The description of the Modifiers Group',
        max_length=512,
        blank=True, null=True
    )
    min_options = models.IntegerField(
        help_text='The minimum amount of the options can be chosen',
        default=0
    )
    max_options = models.IntegerField(
        help_text='The maximum amount of the options can be chosen',
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class ModifiersOption(models.Model):
    group = models.ForeignKey(
        help_text='The modifiers group this option belongs to',
        to='products.ModifiersGroup',
        on_delete=models.CASCADE,
        related_name='options'
    )
    name = models.CharField(
        help_text='The name of the Modifiers Option',
        max_length=32
    )
    price = models.DecimalField(
        help_text='The price of the option',
        max_digits=9, decimal_places=2,
    )
    in_stock = models.BooleanField(
        help_text='Is that option in stock?',
        default=True
    )
    sort_order = SortOrderField(
        help_text='The order of the option in the modifiers group.',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order']


class ProductModifiers(models.Model):
    """
    This model represents relations between ModifiersGroup and ModifiersOption. Basically, extends the ordinary
    auto-generated table for ManyToMany relations, but also additional "sort_order" field. So that relations could be
    ordered.
    """
    product = models.ForeignKey(
        help_text='The product of that relation.',
        to='products.Product',
        on_delete=models.CASCADE,
        # unique=True,
    )
    modifiers_group = models.ForeignKey(
        help_text='The ModifiersGroup of that relation.',
        to='products.ModifiersGroup',
        on_delete=models.CASCADE,
        # unique=True,
    )
    sort_order = SortOrderField(
        help_text='The order of the relation.',
    )

    class Meta:
        ordering = ["sort_order"]
