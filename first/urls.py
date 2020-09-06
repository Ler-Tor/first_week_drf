import requests
from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(http_method_names=['GET'])
def recipient_list(request: Request):
    recipients = []

    try:
        fetched_data = requests.get("https://stepik.org/media/attachments/course/73594/recipients.json").json()
    except TimeoutError:
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    for index in range(len(fetched_data)):
        recipient = {
            "surname": fetched_data[index]["info"]["surname"],
            "name": fetched_data[index]["info"]["name"],
            "patronymic": fetched_data[index]["info"]["patronymic"],
            "phoneNumber": fetched_data[index]["contacts"]["phoneNumber"]
        }
        recipients.append(recipient)
    return Response(data=recipients)


@api_view(http_method_names=['GET'])
def recipient_detail(request: Request, pk: int):
    try:
        fetched_data = requests.get("https://stepik.org/media/attachments/course/73594/recipients.json").json()
    except TimeoutError:
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    for item in fetched_data:
        if int(item['id']) == pk:
            recipient = {
                "surname": item["info"]["surname"],
                "name": item["info"]["name"],
                "patronymic": item["info"]["patronymic"],
                "phoneNumber": item["contacts"]["phoneNumber"]
            }
            return Response(data=recipient)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET'])
def product_set_list(request: Request):
    product_sets = []
    params = request.query_params

    try:
        fetched_data = requests.get("https://stepik.org/media/attachments/course/73594/foodboxes.json").json()
    except TimeoutError:
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    if "min_price" in params:
        for index in range(len(fetched_data)):
            if int(fetched_data[index]["price"]) >= int(params["min_price"]):
                product_set = {
                    "title": fetched_data[index]["name"],
                    "description": fetched_data[index]["about"],
                    "price": fetched_data[index]["price"],
                    "weight": fetched_data[index]["weight_grams"],
                }
                product_sets.append(product_set)
        if not product_sets:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=product_sets)

    elif "min_weight" in params:
        for index in range(len(fetched_data)):
            if int(fetched_data[index]["weight_grams"]) >= int(params["min_weight"]):
                product_set = {
                    "title": fetched_data[index]["name"],
                    "description": fetched_data[index]["about"],
                    "price": fetched_data[index]["price"],
                    "weight": fetched_data[index]["weight_grams"],
                }
                product_sets.append(product_set)
        if not product_sets:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=product_sets)

    else:
        for index in range(len(fetched_data)):
            product_set = {
                "title": fetched_data[index]["name"],
                "description": fetched_data[index]["about"],
                "price": fetched_data[index]["price"],
                "weight": fetched_data[index]["weight_grams"],
            }
            product_sets.append(product_set)
        return Response(data=product_sets)


@api_view(http_method_names=['GET'])
def product_set_detail(request: Request, pk: int):

    try:
        fetched_data = requests.get('https://stepik.org/media/attachments/course/73594/foodboxes.json').json()
    except TimeoutError:
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    for item in fetched_data:
        if int(item["inner_id"]) == pk:
            product_set = {
                "title": item["name"],
                "description": item["about"],
                "price": item["price"],
                "weight": item["weight_grams"],
            }
            return Response(data=product_set)
    return Response(status=status.HTTP_404_NOT_FOUND)


urlpatterns = [
    path('recipients/', recipient_list, name='recipient-list'),
    path('recipients/<int:pk>', recipient_detail, name='recipient-detail'),
    path('product-sets/', product_set_list, name='product-sets'),
    path('product-sets/<int:pk>', product_set_detail, name='product-set-detail'),
]
