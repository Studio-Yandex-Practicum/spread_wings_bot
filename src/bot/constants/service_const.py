import enum

COMMANDS = [
    ("/start", "Запустить/перезапустить бота"),
    ("/help", "Показать, что умеет бот"),
]


class AssistanceTypes(str, enum.Enum):
    """Question types."""

    LEGAL_ASSISTANCE = "Юридическая помощь"
    SOCIAL_ASSISTANCE = "Социальная помощь"
    PSYCHOLOGICAL_ASSISTANCE = "Психологическая помощь"
    COMMON_QUESTION = "Общий вопрос"
