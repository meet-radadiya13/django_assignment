import stripe
from django.db.models.signals import pre_save
from django.dispatch import receiver

from authentication.models import User
from django_assignment import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(pre_save, sender=User)
def add_stripe_customer_id(sender, instance, *args, **kwargs):
    if instance.stripe_customer_id is None and instance.is_owner:
        customer = stripe.Customer.create(
            email=instance.email,
            name=instance.username,
            payment_method="pm_card_visa",
            invoice_settings={
                "default_payment_method": "pm_card_visa",
            }
        )
        instance.stripe_customer_id = customer.id
