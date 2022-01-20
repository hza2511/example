import time

from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase
from tenant_users.tenants.models import UserProfile


def restaurant_image_dir_path(instance, filename: str) -> str:
    """Create the path for the restaurant's image"""
    extension = filename.split('.')[-1]
    new_filename = "restaurants/%s_%i.%s" % (instance, (int(time.time())), extension)

    return new_filename.lower()


class RestaurantInfo(models.Model):
    image = models.ImageField(
        help_text='The image of the restaurant',
        blank=True, null=True,
        upload_to=restaurant_image_dir_path
    )
    # Details
    name = models.CharField(
        help_text='The name of the restaurant',
        max_length=64,
    )
    description = models.TextField(
        help_text='The description of the restaurant',
        max_length=512,
        blank=True, null=True,
    )
    # Contacts
    email = models.EmailField(
        help_text='The email of the restaurant',
        blank=True, null=True,
    )
    phone_number = models.CharField(
        help_text='The phone number of the restaurant',
        max_length=20,
        blank=True, null=True,
    )
    website = models.CharField(
        help_text='The website of the restaurant',
        max_length=2048,
        blank=True, null=True,
    )
    # Store address
    street = models.CharField(
        help_text='The street address of the restaurant',
        max_length=128,
        blank=True, null=True,
    )
    building = models.CharField(
        help_text='The name of the building or the number',
        max_length=32,
        blank=True, null=True
    )
    city = models.CharField(
        help_text='The city of the restaurant',
        max_length=85,
        blank=True, null=True,
    )
    postal_code = models.CharField(
        help_text='The postal code of the restaurant',
        max_length=16,
        blank=True, null=True,
    )
    country = models.CharField(
        help_text='The country of the restaurant',
        max_length=56,
        blank=True, null=True,
    )
    # Messages
    ordering_instructions = models.CharField(
        help_text="We'll show this message to your customers when they first visit your ordering site",
        default='Place your order quick and easy and we will deliver to your table.',
        max_length=512
    )
    no_available_menus = models.CharField(
        help_text="We'll show this message to your customers if you have no available menu.",
        default='We are temporarily not displaying mobile menus, '
                'please use your physical menu or contact our wait staff to order! 😄',
        max_length=512
    )
    # Statuses
    allow_mobile_ordering = models.BooleanField(
        help_text='Are you accepting mobile orders (made with your digital menu)?',
        default=False
    )
    allow_live_payments = models.BooleanField(
        help_text='Are you accepting live payments (paid with your digital menu)?',
        default=False
    )

    class Meta:
        abstract = True


class Restaurant(TenantBase, RestaurantInfo):
    created = models.DateTimeField(
        help_text='When was the restaurant created',
        auto_created=True,
        blank=True, null=True
    )
    modified = models.DateTimeField(
        help_text='When was the restaurant modified last time',
        auto_now=True,
        blank=True, null=True
    )
    owner = models.ForeignKey(
        help_text='The owner of the restaurant',
        to='restaurants.TenantUser',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    is_created = models.BooleanField(
        help_text='If the restaurant creation process has finished',
        default=False
    )

    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):

    def __str__(self):
        return self.domain


class TenantUser(UserProfile):
    # first_name = models.CharField(
    #     help_text="The first name of the user",
    #     max_length=32
    # )
    # middle_name = models.CharField(
    #     help_text="The middle name of the user",
    #     max_length=32,
    #     blank=True, null=True
    # )
    # last_name = models.CharField(
    #     help_text="The last name of the user",
    #     max_length=32
    # )
    full_name = models.CharField(
        help_text='The full name of the user.',
        max_length=128
    )
    phone_number = models.CharField(
        help_text='The phone number of the user',
        max_length=20,
        blank=True, null=True,
        unique=True
    )
