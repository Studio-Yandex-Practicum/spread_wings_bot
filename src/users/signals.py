from django.db.models.signals import post_save
from django.dispatch import receiver
from django_otp.plugins.otp_email.models import EmailDevice

from users.models import User
from users.utils.emailing.reset_password import send_password_reset_email


@receiver(post_save, sender=User)
def password_reset_email(sender, instance, created, **kwargs):
    """Send email to new admin with link to set password."""
    if created:
        EmailDevice.objects.create(
            user=instance,
            email=instance.email,
        )
        if not instance.is_superuser:
            send_password_reset_email(instance)
