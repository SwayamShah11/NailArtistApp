from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile
from customers.models import Customer


@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    CustomerProfile.objects.get_or_create(user=instance)

    if instance.role == "customer":
        Customer.objects.get_or_create(user=instance)
