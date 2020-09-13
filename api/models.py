from django.db import models

# TODO: Описать класс для менеджеров, которые имеют возможность менять статус заказа
# ЛОГИН И ПАРОЛЬ АДМИНКИ admin

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('delivered', 'Delivered'),
    ('processed', 'Processed'),
    ('cancelled', 'Cancelled'),
)


class ProductSets(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    weight = models.BigIntegerField()
    price = models.BigIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'product sets'


class Recipient(models.Model):
    name = models.CharField(max_length=20, null=False)
    surname = models.CharField(max_length=20, null=False)
    patronymic = models.CharField(max_length=20, null=False)
    phone_number = models.CharField(max_length=15)
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s %s" % (self.surname, self.name, self.patronymic)


class Order(models.Model):
    order_created_datetime = models.DateTimeField()
    delivery_datetime = models.DateTimeField()
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT)
    product_set = models.ForeignKey(ProductSets, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
