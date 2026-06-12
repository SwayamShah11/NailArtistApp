from django.shortcuts import (
    render,
    redirect
)

from .models import Customer
from .forms import CustomerForm


def customer_list(request):

    customers = Customer.objects.all()

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': customers
        }
    )


def customer_create(request):

    form = CustomerForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'customer_list'
        )

    return render(
        request,
        'customers/customer_form.html',
        {
            'form': form
        }
    )