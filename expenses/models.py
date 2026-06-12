from django.db import models

CATEGORY_CHOICES = [
    ("RENT", "Rent"),
    ("SALARY", "Salary"),
    ("UTILITIES", "Utilities"),
    ("SUPPLIES", "Nail Supplies"),
    ("MARKETING", "Marketing"),
    ("EQUIPMENT", "Equipment"),
    ("TRAVEL", "Travel"),
    ("OTHER", "Other"),
]


class Expense(models.Model):

    title = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="OTHER",
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    expense_date = models.DateField(null=True, blank=True)

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
