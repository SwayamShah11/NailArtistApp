from django.urls import path

from .views import (
    expense_list,
    expense_create,
)

urlpatterns = [
    path(
        "",
        expense_list,
        name="expense_list",
    ),
    path(
        "create/",
        expense_create,
        name="expense_create",
    ),
]
