import enum

PATTERN = "^{state}$"


class States(str, enum.Enum):
    """Main bot states."""

    ASSISTANCE = "assistance"  # п.с. "Помочь или получить помощь"
    REGION = "region"  # п.с. "Выбор региона"
    ASSISTANCE_TYPE = "assistance_type"  # п.с. "Чем мы можем помочь"
    BACK = "back"
    BACK_TO_REGION = "back_to_region"
    HOME = "home"

    FUND_PROGRAMS = "fund_programs"
    ASK_QUESTION = "ask_question"

    CONTACT_US = "contact_us"
    SELECTED_TYPE = "selected_type"
    SHOW_CONTACT = "show_contact"
