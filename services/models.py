from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete

from clients.models import Client
from .receivers import delete_cache_total_sum
from .tasks import set_price


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._full_price = instance.full_price
        return instance

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.full_price != getattr(self, '_full_price', None):
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

    def __str__(self):
        return self.name


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(100)
    ])

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._discount_percent = instance.discount_percent
        return instance

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.discount_percent != getattr(self, '_discount_percent', None):
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

    def __str__(self):
        return f'Plan->{self.plan_type}'


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Subscription -> [{self.client} - {self.plan}]'


post_delete.connect(delete_cache_total_sum, sender=Subscription)
