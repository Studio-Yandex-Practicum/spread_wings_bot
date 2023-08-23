import re

from django.core.validators import RegexValidator

from bot.constants.validation import (
    PHONE,
    PHONE_FORMAT,
    PHONE_PATTERN,
    TELEGRAM_FORMAT,
    TELEGRAM_USERNAME,
)

phone_regex = RegexValidator(
    regex=PHONE, message=f"Введите номер телефона в формате: {PHONE_FORMAT}"
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
