import enum


class AskQuestionStates(str, enum.Enum):
    """Ask question states."""

    QUESTION = "question"
    NAME = "name"
    CONTACT_TYPE = "contact_type"
    ENTER_YOUR_CONTACT = "enter_your_contact"
    END = "end"
