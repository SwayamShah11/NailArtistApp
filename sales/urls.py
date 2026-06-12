from django.urls import path
from . import views

urlpatterns = [
    path("", views.sale_list, name="sale_list"),

    path(
        "create/",
        views.sale_create,
        name="sale_create",
    ),

    path(
        "api/product/<int:pk>/",
        views.product_price,
        name="product_price",
    ),

    path(
        "api/service/<int:pk>/",
        views.service_price,
        name="service_price",
    ),
]