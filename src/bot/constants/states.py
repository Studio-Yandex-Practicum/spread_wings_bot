import enum


PATTERN = "^{state}$"


class States(str, enum.Enum):
    """Состояния бота."""

    ASSISTANCE = "assistance"  # п.с. "Помочь или получить помощь"
    DONATION = "donation"  # п.с. "Перенаправление на форму с пожертвованиями"
    REGION = "region"  # п.с. "Выбор региона"
    ASSISTANCE_TYPE = 'assistance_type'  # п.с. "Чем мы можем помочь"
    BACK = "back"
    BACK_TO_REGION = "back_to_region"

    LEGAL_ASSISTANCE = "legal_assistance"
    SOCIAL_ASSISTANCE = "social_assistance"
    PSYCHOLOGICAL_ASSISTANCE = "psychological_assistance"
    FUND_PROGRAMS = "fund_programs"
    CONTACT_US = "contact_us"
