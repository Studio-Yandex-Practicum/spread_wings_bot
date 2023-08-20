import enum


class States(str, enum.Enum):
    """Main bot states."""

    ASSISTANCE_TYPE = "assistance_type"
    CONTACT_TYPE = "contact_type"
    CONTACT_US = "contact_us"
    FUND_PROGRAMS = "fund_programs"
    GET_ASSISTANCE = "get_assistance"
    GET_CONTACT = "get_contact"
    GET_CONTACT_TYPE = "get_contact_type"
    GET_USERNAME = "get_user_name"
    GET_USER_QUESTION = "get_user_question"
    REGION = "region"
    SEND_EMAIL = "send_email"
    SHOW_CONTACT = "show_contact"
