from django.shortcuts import (
    render,
    redirect
)

from .models import Supplier
from .forms import SupplierForm


def supplier_list(request):

    suppliers = Supplier.objects.all()

    return render(
        request,
        'suppliers/supplier_list.html',
        {
            'suppliers': suppliers
        }
    )


def supplier_create(request):

    form = SupplierForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'supplier_list'
        )

    return render(
        request,
        'suppliers/supplier_form.html',
        {
            'form': form
        }
    )