from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from utils.emailing.reset_password import send_password_reset_email


@receiver(post_save, sender=User)
def password_reset_email(sender, instance, created, **kwargs):
    """Send email to new admin with link to set password."""
    if created and instance.is_staff and not instance.is_superuser:
        send_password_reset_email(instance)
