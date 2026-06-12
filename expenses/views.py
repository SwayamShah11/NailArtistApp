from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):

    expenses = Expense.objects.order_by(
        "-expense_date",
        "-created_at"
    )

    return render(
        request,
        "expenses/expense_list.html",
        {
            "expenses": expenses
        }
    )


@login_required
def expense_create(request):

    form = ExpenseForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            "expense_list"
        )

    return render(
        request,
        "expenses/expense_form.html",
        {
            "form": form
        }
    )
