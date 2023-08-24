import enum


class States(str, enum.Enum):
    """Main bot states."""

    GET_ASSISTANCE = "get_assistance"  # п.с. "Помочь или получить помощь"
    REGION = "region"  # п.с. "Выбор региона"
    ASSISTANCE_TYPE = "assistance_type"  # п.с. "Чем мы можем помочь"
    FUND_PROGRAMS = "fund_programs"
    GET_USER_QUESTION = "get_user_question"
    CONTACT_US = "contact_us"
    SHOW_CONTACT = "show_contact"
    GET_USERNAME = "get_username"
    QUESTION_TYPE = "question_type"
    USERNAME_AFTER_RETURNING = "username_after_returning"
    SEND_EMAIL = "send_email"
    GET_CONTACT = "get_contact"
    SHOW_PROGRAM = "show_program"
    SHOW_QUESTION = "show_question"
