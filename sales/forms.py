from django import forms
from django.forms import inlineformset_factory

from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = ["customer"]


class SaleItemForm(forms.ModelForm):

    class Meta:
        model = SaleItem
        fields = [
            "product",
            "service",
            "quantity",
            "price",
        ]


SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=5,          # Show 5 blank rows initially
    can_delete=True   # Allow removing rows
)