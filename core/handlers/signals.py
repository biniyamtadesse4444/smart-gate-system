from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Card
from .services import add_card_to_device


@receiver(post_save, sender=Card)
def send_card_to_device(sender, instance, created, **kwargs):

    if created:
        add_card_to_device(
            instance.card_number,
            instance.pin,
            instance.index,
            instance.expire_year,
            instance.expire_month,
            instance.expire_day
        )

    # CASE 2: Payment updated
    elif instance.is_paid:
        add_card_to_device(
            instance.card_number,
            instance.pin,
            instance.index,
            instance.expire_year,
            instance.expire_month,
            instance.expire_day
        )