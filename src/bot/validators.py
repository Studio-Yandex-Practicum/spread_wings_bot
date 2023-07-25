from django.core.validators import RegexValidator

TELEGRAM_USERNAME = r"^[\w\_]{5,32}$"
PHONE = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"

phone_regex = RegexValidator(regex=PHONE)
telegram_regex = RegexValidator(regex=TELEGRAM_USERNAME)