from django.db import models
from products.models import Product
from django.core.exceptions import ValidationError

TRANSACTION_TYPES = (
        ('PURCHASE', 'Purchase'),
        ('SALE', 'Sale'),
        ('ADJUSTMENT', 'Adjustment'),
    )


class InventoryTransaction(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        null=True,
        blank=True
    )

    quantity = models.IntegerField(null=True, blank=True)

    reference_id = models.IntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        return f"{product_name} - {self.transaction_type}"

    def clean(self):
        if self.quantity == 0:
            raise ValidationError(
                "Quantity cannot be zero."
            )
