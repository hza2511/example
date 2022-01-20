from django.db import models


# Create your models here.
class Order(models.Model):
    # TODO: table = mo
    payment_method = models.CharField(
        help_text='The payment used to complete that order.',
        max_length=128
    )
    created = models.DateTimeField(
        help_text='When was the order placed.',
        auto_created=True,
        auto_now=True,
        blank=True, null=True
    )
    # TODO: customer info


class OrderItem(models.Model):
    order = models.ForeignKey(
        help_text='The order that item belongs to.',
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='items',
    )
