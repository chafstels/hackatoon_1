from celery import shared_task
from django.db import transaction
from django.db.models import F
from celery_singleton import Singleton
from django.core.cache import cache
from django.conf import settings


@shared_task(base=Singleton)
def set_price(subscription_id):
    from .models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.filter(id=subscription_id).annotate(annotated_price=F('service__full_price') -
                  F('service__full_price') * F('plan__discount_percent') / 100.0).first()

        subscription.price = subscription.annotated_price
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)

