from django import forms

from .models import InventoryTransaction


class StockAdjustmentForm(forms.ModelForm):

    class Meta:
        model = InventoryTransaction
        fields = (
            "product",
            "quantity",
        )

    def save(self, commit=True):

        obj = super().save(commit=False)

        obj.transaction_type = "ADJUSTMENT"

        if commit:
            obj.save()

        return obj

    def clean_quantity(self):
        qty = self.cleaned_data["quantity"]

        if qty == 0:
            raise forms.ValidationError(
                "Quantity cannot be zero."
            )

        return qty