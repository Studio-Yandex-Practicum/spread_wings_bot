import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import bot.models as models
from bot.constants.validation import (
    PHONE,
    PHONE_PATTERN,
    TELEGRAM_FORMAT,
    TELEGRAM_USERNAME,
)

phone_regex = RegexValidator(
    regex=PHONE, message="Введите номер телефона в формате: +7 (777) 777-77-77"
)
telegram_regex = RegexValidator(
    regex=TELEGRAM_USERNAME,
    message=f"Введите название аккаунта telegram в формате: {TELEGRAM_FORMAT}",
)


def format_phone_number(phone):
    """Format the phone number."""
    digits = re.sub(r"\D", "", phone)
    start_index = 0
    if digits.startswith("7") or digits.startswith("8"):
        start_index = 1

    replacements = list(digits[start_index:])

    formatted = re.sub(r"X", lambda match: replacements.pop(0), PHONE_PATTERN)
    return formatted


def format_telegram_link(telegram):
    """Format the telegram link."""
    return "https://t.me/" + telegram


def validate_is_chief(value):
    """Validate that the Chief coordinator may be only one."""
    if value and models.Coordinator.objects.filter(is_chief=True).exists():
        raise ValidationError("Может быть только один Главный координатор!")
