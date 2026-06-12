from django.db import models
from customers.models import Customer
from products.models import Product
from inventory.models import InventoryTransaction
from django.core.exceptions import ValidationError


class Service(models.Model):

    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    duration_minutes = models.IntegerField(
        default=60,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name



class Sale(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    sale_date = models.DateTimeField(
        auto_now_add=True
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Sale #{self.id}"

    def update_total(self):
        total = sum(
            item.subtotal
            for item in self.items.all()
        )

        self.total_amount = total

        self.save()


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True
    )

    price = models.DecimalField(
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


    def clean(self):
        if not self.product and not self.service:
            raise ValidationError(
                "Select either a product or a service."
            )

        if self.product and self.service:
            raise ValidationError(
                "A sale item cannot be both a product and a service."
            )

        if self.product:
            if self.product.current_stock < self.quantity:
                raise ValidationError(
                    f"Only {self.product.current_stock} units available."
                )

    def save(self, *args, **kwargs):

        self.subtotal = self.quantity * self.price

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and self.product:
            InventoryTransaction.objects.create(
                product=self.product,
                transaction_type='SALE',
                quantity=-self.quantity,
                reference_id=self.sale.id
            )

        self.sale.update_total()
