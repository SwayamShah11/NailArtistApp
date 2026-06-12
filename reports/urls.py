from django.urls import path
from .views import accounting_summary

urlpatterns = [
    path(
        "accounting/",
        accounting_summary,
        name="accounting_summary",
    ),
]