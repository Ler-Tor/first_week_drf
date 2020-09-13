from django.contrib import admin
from .models import ProductSets, Recipient, Order

admin.site.register(ProductSets)
admin.site.register(Recipient)
admin.site.register(Order)
# Register your models here.
