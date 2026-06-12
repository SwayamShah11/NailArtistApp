from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.inventory_list,
        name="inventory_list",
    ),
    path(
        "adjust/",
        views.stock_adjustment,
        name="stock_adjustment",
    ),
    path(
        "history/",
        views.inventory_history,
        name="inventory_history",
    ),
    path(
        "product/<int:product_id>/",
        views.product_inventory_detail,
        name="product_inventory_detail",
    ),
    path(
        "export/csv/",
        views.export_inventory_csv,
        name="export_inventory_csv",
    ),
]