from django.contrib import admin

from .models import (
    Service,
    Sale,
    SaleItem
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price'
    )


class SaleItemInline(
    admin.TabularInline
):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer',
        'sale_date',
        'total_amount'
    )

    inlines = [
        SaleItemInline
    ]