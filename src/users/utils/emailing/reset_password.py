import os

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config import settings
from users.models import User
from users.utils.emailing.render import render_email_message


def send_password_reset_email(instance: User, message=None, template=None):
    """Send email with password reset link."""
    if template is None:
        template = "emailing/password_reset_email.html"
    reset_link = get_password_reset_link(instance)
    email = render_email_message(
        subject='Доступ к админ-панели бота "Расправь крылья"',
        context={"password_reset_link": reset_link, "message": message},
        from_email=settings.EMAIL_HOST_USER,
        to=[
            instance.email,
        ],
        template=template,
    )
    email.send(fail_silently=False)


def get_password_reset_link(instance):
    """Generate password reset link."""
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    token = default_token_generator.make_token(instance)
    reset_url = reverse("users:password_set", args=[uid, token])
    return (
        f"http://{os.environ.get('NGINX_HOST', '127.0.0.1')}:"
        f"{os.environ.get('NGINX_PORT', '8000')}{reset_url}"
    )
