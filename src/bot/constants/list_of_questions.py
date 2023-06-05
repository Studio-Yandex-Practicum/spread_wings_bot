import enum


class LegalQuestions(str, enum.Enum):
    """Question list."""

    FIRST_QUESTION = "[Заглушка]Первый вопрос"
    SECOND_QUESTION = "[Заглушка]Второй вопрос"
    THIRD_QUESTION = "[Заглушка]Третий вопрос"
