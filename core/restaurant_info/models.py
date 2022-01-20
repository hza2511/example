from django.db import models
import uuid


# Create your models here.
class WorkingDay(models.Model):
    name = models.CharField(
        help_text='The name of the day of the week',
        max_length=9,
        editable=False
    )
    weekday = models.IntegerField(
        help_text='The number of the day of the week. 1 - Monday, 7 - Sunday',
        editable=False
    )
    open_24 = models.BooleanField(
        help_text='Is the restaurant opened all the day?',
        default=False
    )
    closed = models.BooleanField(
        help_text='Is the restaurant closed all the day?',
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class WorkingHours(models.Model):
    working_day = models.ForeignKey(
        help_text='The working day working hours are related to',
        on_delete=models.CASCADE,
        to='restaurant_info.WorkingDay',
        related_name='working_hours'
    )
    opens = models.TimeField(
        help_text='The time restaurant opens at'
    )
    closes = models.TimeField(
        help_text='The time restaurant closes at'
    )

    def __str__(self):
        return f'{self.opens} to {self.closes}'

    class Meta:
        ordering = ['id']


class Area(models.Model):
    name = models.CharField(
        help_text='The name of the area (venue)',
        max_length=32,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Table(models.Model):
    area = models.ForeignKey(
        help_text='The area that table belongs to',
        to='restaurant_info.Area',
        on_delete=models.CASCADE,
        related_name='tables'
    )
    name = models.CharField(
        help_text='The name of the table',
        max_length=32
    )
    # link = models.CharField(
    #     help_text='The link related to that table. Based on the subdomain',
    #     max_length=2048,
    # )
    # file = models.FileField(
    #     help_text='The QR Code file'
    # )
    # uuid = models.UUIDField(
    #     default=uuid.uuid4,
    #     unique=True,
    #     editable=False
    #     # Todo: Use as PK?
    # )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
