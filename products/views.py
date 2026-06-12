from django.shortcuts import render
from .models import Product
from django.shortcuts import redirect
from .forms import ProductForm

def product_list(request):

    products = Product.objects.all()

    return render(
        request,
        'products/product_list.html',
        {
            'products': products
        }
    )


def product_create(request):

    form = ProductForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'product_list'
        )

    return render(
        request,
        'products/product_form.html',
        {
            'form': form
        }
    )