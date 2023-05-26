import enum


class States(str, enum.Enum):
    """Состояния бота."""

    ASSISTANCE = "assistance"  # п.с. "Помочь или получить помощь"
    DONATION = "donation"  # п.с. "Перенаправление на форму с пожертвованиями"
    REGION = "region"  # п.с. "Выбор региона"


# Patterns $ callback_data, переменные создал для
# InlineKeyboardButton.callback_data и
# CallbackQueryHandler.pattern, чтобы их связать.
PATTERN = "^{state}$"

HELP = "make_donation"
GET_HELP = "receive_assistance"
BACK = "back"
