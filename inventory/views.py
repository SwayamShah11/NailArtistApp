from products.models import Product
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import StockAdjustmentForm
from .models import InventoryTransaction
import csv
from django.http import HttpResponse


def inventory_list(request):

    query = request.GET.get("q", "")

    products = Product.objects.all()

    if query:
        products = products.filter(
            name__icontains=query
        )

    products = products.order_by("name")

    low_stock_count = sum(
        1
        for product in products
        if product.current_stock <= product.minimum_stock
    )

    return render(
        request,
        "inventory/inventory_list.html",
        {
            "products": products,
            "query": query,
            "low_stock_count": low_stock_count,
        },
    )


def inventory_history(request):

    transactions = (
        InventoryTransaction.objects
        .select_related("product")
        .order_by("-created_at")
    )

    return render(
        request,
        "inventory/inventory_history.html",
        {
            "transactions": transactions,
        },
    )


def product_inventory_detail(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id
    )

    transactions = (
        product.transactions
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "inventory/product_inventory_detail.html",
        {
            "product": product,
            "transactions": transactions,
        },
    )


def stock_adjustment(request):

    form = StockAdjustmentForm(
        request.POST or None
    )

    if form.is_valid():

        adjustment = form.save(
            commit=False
        )

        adjustment.transaction_type = "ADJUSTMENT"

        if adjustment.quantity == 0:
            messages.error(
                request,
                "Quantity cannot be zero."
            )
            return render(
                request,
                "inventory/stock_adjustment.html",
                {
                    "form": form,
                },
            )

        current_stock = adjustment.product.current_stock

        if current_stock + adjustment.quantity < 0:
            messages.error(
                request,
                f"Only {current_stock} items available in stock."
            )
            return render(
                request,
                "inventory/stock_adjustment.html",
                {
                    "form": form,
                },
            )

        adjustment.save()

        messages.success(
            request,
            "Stock adjusted successfully."
        )

        return redirect(
            "inventory_list"
        )

    return render(
        request,
        "inventory/stock_adjustment.html",
        {
            "form": form,
        },
    )


def export_inventory_csv(request):

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)

    writer.writerow(
        [
            "Product",
            "Current Stock",
            "Minimum Stock",
        ]
    )

    for product in Product.objects.all():

        writer.writerow(
            [
                product.name,
                product.current_stock,
                product.minimum_stock,
            ]
        )

    return response