import logging
from typing import Sequence

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.validators import MailValidator


logger = logging.getLogger("core")


async def send_email(
    subject: str,
    message: str,
    recipients: Sequence[str] = None,
) -> None:
    """Send email to recipients through Django."""
    if not recipients:
        recipients = [settings.DEFAULT_RECEIVER]

    mail = MailValidator(**locals())
    template = get_template(settings.EMAIL_TEMPLATE_NAME)
    html_content = template.render(
        {"message": mail.message, "subject": mail.subject}
    )
    message = EmailMultiAlternatives(
        subject=mail.subject,
        body=mail.message,
        from_email=settings.EMAIL_HOST_USER,
        to=mail.recipients,
    )
    message.attach_alternative(html_content, "text/html")

    try:
        logger.info(
            f"Sending email to recipients: {', '.join(mail.recipients)}..."
        )
        await sync_to_async(message.send)()
    except Exception as e:
        logger.error(f"Error while sending email: {e}")
    else:
        logger.info("Email has been sent successfully")
