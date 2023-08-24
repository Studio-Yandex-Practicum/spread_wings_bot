from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config import settings
from users.models import User


@receiver(post_save, sender=User)
def send_password_reset_email(sender, instance, created, **kwargs):
    """Send email to new admin with link to set password."""
    if created and instance.is_superuser:
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = token_generator.make_token(instance)
        reset_url = reverse("password_reset", args=[uid, token])

        subject = "Password change Link"
        message = render_to_string(
            "registration/password_change_form.html",
            {
                "user": instance,
                "reset_url": reset_url,
            },
        )
        from_email = settings.EMAIL_HOST_USER
        instance.email_user(subject, message, from_email)
