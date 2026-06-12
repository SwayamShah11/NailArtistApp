from django.db.models import Sum
from django.shortcuts import render
from appointments.models import Appointment
from customers.models import Customer
from products.models import Product
from purchases.models import Purchase
from sales.models import Sale
from suppliers.models import Supplier
from inventory.models import InventoryTransaction


def home(request):

    products = Product.objects.all()

    low_stock_products = [
        product
        for product in products
        if 0 < product.current_stock <= product.minimum_stock
    ]

    out_of_stock_products = [
        product
        for product in products
        if product.current_stock <= 0
    ]

    recent_inventory = (
        InventoryTransaction.objects
        .select_related("product")
        .order_by("-created_at")[:5]
    )

    context = {
        "total_products": Product.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_suppliers": Supplier.objects.count(),
        "total_sales": Sale.objects.count(),
        "total_purchases": Purchase.objects.count(),

        "pending_appointments": Appointment.objects.filter(
            status="PENDING"
        ).count(),

        "revenue": Sale.objects.aggregate(
            total=Sum("total_amount")
        )["total"] or 0,

        "purchase_cost": Purchase.objects.aggregate(
            total=Sum("total_amount")
        )["total"] or 0,

        # Inventory KPIs
        "low_stock_count": len(low_stock_products),
        "out_of_stock_count": len(out_of_stock_products),
        "recent_inventory": recent_inventory,
        "total_inventory_transactions": InventoryTransaction.objects.count(),
    }

    context["profit"] = (
        context["revenue"]
        - context["purchase_cost"]
    )

    return render(
        request,
        "dashboard/home.html",
        context,
    )
