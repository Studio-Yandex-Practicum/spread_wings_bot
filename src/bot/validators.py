from django.core.validators import RegexValidator

EMAIL = r"[^@]+@[^@]+\.[^@]+"
PHONE = r"^((\+7|7|8)+([0-9]){10})$"
PHONE_FORMAT = "+7 777 777 77 77"
TELEGRAM_FORMAT = "username"
TELEGRAM_USERNAME = r"^[\w\_]{5,32}$"
phone_regex = RegexValidator(
    regex=PHONE, message=f"Введите номер телефона в формате: {PHONE_FORMAT}"
)
telegram_regex = RegexValidator(
    regex=TELEGRAM_USERNAME,
    message=f"Введите название аккаунта telegram в формате: {TELEGRAM_FORMAT}",
)


def format_phone_number(phone):
    """Format the phone number."""

    formatted = ""
    i = 0

    phone = "".join(x for x in phone if x.isdigit())
    if phone[0] == "+":
        phone = phone[2:]
    else:
        phone = phone[1:]
    pattern = "+ 7 (XXX) XXX-XX-XX"
    phone = phone[::-1]
    pattern = pattern[::-1]
    for p in range(len(pattern)):
        if pattern[p] != "X":
            formatted += pattern[p]
            continue
        formatted += phone[i]
        i += 1
    formatted = formatted[::-1]
    return formatted


def format_telegram_link(telegram):
    """Format the telegram link."""

    return "https://t.me/" + telegram
