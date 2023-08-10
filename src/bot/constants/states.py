import enum


# States
class States(str, enum.Enum):
    """Main bot states."""

    ASSISTANCE = "assistance"  # п.с. "Помочь или получить помощь"
    REGION = "region"  # п.с. "Выбор региона"
    ASSISTANCE_TYPE = "assistance_type"  # п.с. "Чем мы можем помочь"
    FUND_PROGRAMS = "fund_programs"
    ASK_QUESTION = "ask_question"
    CONTACT_US = "contact_us"
    QUESTIONS_AND_CONTACTS = "selected_type"
    SHOW_CONTACT = "show_contact"
    QUESTION = "question"
    NAME = "name"
    CONTACT_TYPE = "contact_type"
    ENTER_YOUR_CONTACT = "enter_your_contact"
    END = "end"


# Patterns
PATTERN = "^{state}$"

MESSAGE_PATTERN = r"^[^\/].*$"
BACK = r"back_to_"
CONTACT = PATTERN.format(state="EMAIL|PHONE|TELEGRAM")
HELP_TYPE = PATTERN.format(
    state="LEGAL_ASSISTANCE|SOCIAL_ASSISTANCE|" "PSYCHOLOGICAL_ASSISTANCE"
)
CONTACT_TYPE = PATTERN.format(state=States.CONTACT_TYPE.value)
ASK_QUESTION = PATTERN.format(state=States.ASK_QUESTION.value)
ASSISTANCE = PATTERN.format(state=States.ASSISTANCE.value)
FUND_PROGRAMS = PATTERN.format(state=States.FUND_PROGRAMS.value)
CONTACT_US = PATTERN.format(state=States.CONTACT_US.value)
SHOW_CONTACT = PATTERN.format(state=States.SHOW_CONTACT.value)
