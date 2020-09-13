from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator
from .models import Order, ProductSets, Recipient


ORDER_STATUS_CHOICES = {
    'created',
    'delivered',
    'processed',
    'cancelled',
}


class RecipientSerializer(ModelSerializer):
    def check_is_null(self, value):
        if value is None:
            raise ValidationError("Can not be empty")
        return value

    def validate_name(self, value):
        return self.check_is_null(value)

    def validate_surname(self, value):
        return self.check_is_null(value)

    def validate_patronymic(self, value):
        return self.check_is_null(value)

    class Meta:
        model = Recipient
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Recipient.objects.all(),
                fields=['name', 'surname', 'patronymic']
            )
        ]


class ProductSetsSerializer(ModelSerializer):
    class Meta:
        model = ProductSets
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    def validate_status(self, value):
        if value in ORDER_STATUS_CHOICES:
            return value
        else:
            raise ValidationError("Unknown status")

    class Meta:
        model = Order
        fields = '__all__'
