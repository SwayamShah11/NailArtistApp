from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from sales.models import Sale
from purchases.models import Purchase
from expenses.models import Expense


@login_required
def accounting_summary(request):

    total_sales = (
        Sale.objects.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    total_purchases = (
        Purchase.objects.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    total_expenses = (
        Expense.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    estimated_profit = (
        total_sales
        - total_purchases
        - total_expenses
    )

    context = {
        "total_sales": total_sales,
        "total_purchases": total_purchases,
        "total_expenses": total_expenses,
        "estimated_profit": estimated_profit,
    }

    return render(
        request,
        "reports/accounting_summary.html",
        context,
    )