from django.db import models
from suppliers.models import Supplier
from products.models import Product
from inventory.models import InventoryTransaction


class Purchase(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    purchase_date = models.DateField(null=True, blank=True)

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Purchase #{self.id}"

    def update_total(self):
        total = sum(
            item.subtotal
            for item in self.items.all()
        )

        self.total_amount = total

        self.save()


class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
        null=True, blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(null=True, blank=True)

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        self.subtotal = self.quantity * self.price

        is_new = self.pk is None

        if is_new and self.product:

            if self.product.current_stock < self.quantity:
                raise ValueError(
                    "Not enough stock available"
                )

        super().save(*args, **kwargs)

        if is_new and self.product:
            InventoryTransaction.objects.create(
                product=self.product,
                transaction_type='SALE',
                quantity=-self.quantity,
                reference_id=self.sale.id
            )
            self.purchase.update_total()