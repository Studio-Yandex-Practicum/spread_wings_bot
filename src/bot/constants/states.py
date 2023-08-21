import enum


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
    SHOW_PROGRAM = "show_program"
    SHOW_QUESTION = "show_question"
