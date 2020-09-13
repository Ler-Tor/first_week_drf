from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSetsSerializer, RecipientSerializer, OrderSerializer
from .models import ProductSets, Order, Recipient
from .filters import OrderFilter


ERROR_MESSAGE = {
    "ERROR": "INVALID SCHEMA"
}

CHOICE_MESSAGE = {
    "ERROR": "INVALID SCHEMA",
    "available choices": ['created', 'delivered', 'processed', 'cancelled']

}


DELETE_ORDER_MESSAGE = {
    "info": "Unable to delete. Only status modification can be applied. Please, use link below.",
    "url": "http://127.0.0.1:8000/api/orders/1/change-status/"
}


def data_saver(fetched_data, query_object, serializer_name):
    serializer = serializer_name(query_object, data=fetched_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipientViewSet(ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer

    def partial_update(self, request, pk=None):
        recipient = self.get_object()
        if 'phone_number' in request.data and len(request.data) == 1:
            return data_saver(fetched_data=request.data, query_object=recipient, serializer_name=self.serializer_class)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=ERROR_MESSAGE)

    @action(methods=['patch'], detail=True, url_path='change-name',
            url_name='change_name')
    def change_name(self, request, pk=None):
        recipient = self.get_object()

        if 'name' and 'surname' and 'patronymic' in request.data and len(request.data) == 3:
            return data_saver(fetched_data=request.data, query_object=recipient, serializer_name=self.serializer_class)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=ERROR_MESSAGE)

    @action(methods=['patch'], detail=True, url_path='change-address',
            url_name='change_address')
    def change_address(self, request, pk=None):
        recipient = self.get_object()

        if 'delivery_address' in request.data and len(request.data) == 1:
            return data_saver(fetched_data=request.data, query_object=recipient, serializer_name=self.serializer_class)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=ERROR_MESSAGE)


class ProductSetsViewSet(ReadOnlyModelViewSet):
    queryset = ProductSets.objects.all()
    serializer_class = ProductSetsSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN, data=DELETE_ORDER_MESSAGE)

    @action(methods=['patch'], detail=True, url_path='change-status',
            url_name='change_status')
    def change_status(self, request, pk=None):
        order = self.get_object()
        if 'status' in request.data and len(request.data) == 1:
            return data_saver(fetched_data=request.data, query_object=order, serializer_name=self.serializer_class)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=CHOICE_MESSAGE)
