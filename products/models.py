from django.db import models
from django.db.models import Sum


class Product(models.Model):

    name = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    minimum_stock = models.PositiveIntegerField(
        default=5,
        null=True,
        blank=True
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name or f"Product {self.id}"

    @property
    def current_stock(self):
        return sum(
            transaction.quantity or 0
            for transaction in self.transactions.all()
        )
