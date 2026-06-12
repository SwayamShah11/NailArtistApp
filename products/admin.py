from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'current_stock',
        'purchase_price',
        'selling_price'
    )

    search_fields = (
        'name',
    )
