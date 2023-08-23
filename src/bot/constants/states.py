import enum


class States(str, enum.Enum):
    """Main bot states."""

    GET_ASSISTANCE = "get_assistance"  # п.с. "Помочь или получить помощь"
    REGION = "region"  # п.с. "Выбор региона"
    ASSISTANCE_TYPE = "assistance_type"  # п.с. "Чем мы можем помочь"
    FUND_PROGRAMS = "fund_programs"
    GET_USER_QUESTION = "get_user_question"
    CONTACT_US = "contact_us"
    QUESTIONS_AND_CONTACTS = "selected_type"
    SHOW_CONTACT = "show_contact"
    GET_USERNAME = "get_username"
    QUESTION_TYPE = "question_type"
    USERNAME_AFTER_RETURNING = "username_after_returning"
    CONTACT_TYPE = "contact_type"
    ENTER_YOUR_CONTACT = "enter_your_contact"
    END = "end"
    SHOW_PROGRAM = "show_program"
