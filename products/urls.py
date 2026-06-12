from django.urls import path
from .views import (
    product_list,
    product_create
)

urlpatterns = [

    path(
        '',
        product_list,
        name='product_list'
    ),

    path(
        'create/',
        product_create,
        name='product_create'
    ),
]