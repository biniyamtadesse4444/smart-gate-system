from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Customer)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            phone_number=instance.phone_number,  # ✅ REQUIRED
            is_active=True
        )
        instance.user = user
        instance.save(update_fields=['user'])
    else:
        if instance.user:
            User.objects.filter(pk=instance.user.pk).update(
                phone_number=instance.phone_number  # ✅ keep in sync
            )
