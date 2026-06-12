from django.urls import path

from .views import (
    customer_list,
    customer_create
)

urlpatterns = [

    path(
        '',
        customer_list,
        name='customer_list'
    ),

    path(
        'create/',
        customer_create,
        name='customer_create'
    ),
]