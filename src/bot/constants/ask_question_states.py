import enum


class AskQuestionStates(str, enum.Enum):
    """Состояния бота."""

    QUESTION = "question"
    NAME = "name"
    CONTACT_TYPE = "contact_type"
    ENTER_YOUR_CONTACT = "enter_your_contact"
    END = "end"
