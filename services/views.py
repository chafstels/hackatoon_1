from django.db.models import Prefetch, F, Sum, Count
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer
from clients.models import Client
from django.core.cache import cache
from django.conf import settings


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only('company_name', 'user__email'))
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)


        price_cache = cache.get(settings.PRICE_CACHE_NAME)
        # subscription_quantity_cache = cache.get('subscription_quantity_cache')
        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60*60)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response_data['subscription_quantity'] = queryset.aggregate(quantity=Count('id')).get('quantity')
        response.data = response_data
        return response
