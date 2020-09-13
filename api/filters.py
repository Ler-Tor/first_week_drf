from django_filters import rest_framework as filters
from .models import Order
from django.db import models


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'delivery_datetime': ['lt', 'gt'],
            'order_created_datetime': ['lt', 'gt'],
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': filters.DateTimeFilter
            }
        }

# ЛОГИН И ПАРОЛЬ АДМИНКИ admin