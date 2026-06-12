from django.shortcuts import render, redirect
from .forms import SaleForm, SaleItemFormSet
from .models import Sale, SaleItem, Service
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.models import Product
from customers.models import Customer
from inventory.models import InventoryTransaction
from django.db import transaction
import json
from django.contrib import messages
from collections import defaultdict


def sale_list(request):

    sales = Sale.objects.all()

    return render(
        request,
        'sales/sale_list.html',
        {
            'sales': sales
        }
    )


def product_price(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return JsonResponse({
        "price": float(product.selling_price or 0)
    })


def service_price(request, pk):
    service = get_object_or_404(Service, pk=pk)

    return JsonResponse({
        "price": float(service.price or 0)
    })


def sale_create(request):

    if request.method == "POST":

        try:
            customer = Customer.objects.get(
                pk=request.POST.get("customer")
            )

            invoice = json.loads(
                request.POST.get("invoice_data", "[]")
            )

        except Exception:

            messages.error(
                request,
                "Invalid invoice data."
            )

            return render(
                request,
                "sales/sale_create.html",
                {
                    "customers": Customer.objects.all(),
                    "products": Product.objects.all(),
                    "services": Service.objects.all(),
                },
            )

        # ----------------------------
        # VALIDATION PHASE
        # ----------------------------

        if not invoice:

            messages.error(
                request,
                "Please add at least one item."
            )

            return render(
                request,
                "sales/sale_create.html",
                {
                    "customers": Customer.objects.all(),
                    "products": Product.objects.all(),
                    "services": Service.objects.all(),
                },
            )

        requested_products = defaultdict(int)

        for row in invoice:

            try:
                qty = int(row["quantity"])
            except Exception:
                qty = 0

            if qty <= 0:

                messages.error(
                    request,
                    "Quantity must be greater than zero."
                )

                return render(
                    request,
                    "sales/sale_create.html",
                    {
                        "customers": Customer.objects.all(),
                        "products": Product.objects.all(),
                        "services": Service.objects.all(),
                    },
                )

            if row["type"] == "product":

                requested_products[
                    int(row["id"])
                ] += qty

        # Validate total stock required
        for product_id, required_qty in requested_products.items():

            product = Product.objects.get(
                pk=product_id
            )

            if required_qty > product.current_stock:

                messages.error(
                    request,
                    f"'{product.name}' has only "
                    f"{product.current_stock} unit(s) available "
                    f"but {required_qty} were requested."
                )

                return render(
                    request,
                    "sales/sale_create.html",
                    {
                        "customers": Customer.objects.all(),
                        "products": Product.objects.all(),
                        "services": Service.objects.all(),
                    },
                )

        # ----------------------------
        # SAVE PHASE
        # ----------------------------

        with transaction.atomic():

            sale = Sale.objects.create(
                customer=customer
            )

            total = 0

            for row in invoice:

                qty = int(row["quantity"])
                price = float(row["price"])
                subtotal = qty * price

                if row["type"] == "product":

                    product = Product.objects.get(
                        pk=row["id"]
                    )

                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=qty,
                        price=price,
                        subtotal=subtotal,
                    )

                else:

                    service = Service.objects.get(
                        pk=row["id"]
                    )

                    SaleItem.objects.create(
                        sale=sale,
                        service=service,
                        quantity=qty,
                        price=price,
                        subtotal=subtotal,
                    )

                total += subtotal

            sale.total_amount = total
            sale.save()

        messages.success(
            request,
            "Sale created successfully."
        )

        return redirect("sale_list")

    return render(
        request,
        "sales/sale_create.html",
        {
            "customers": Customer.objects.all(),
            "products": Product.objects.all(),
            "services": Service.objects.all(),
        },
    )
