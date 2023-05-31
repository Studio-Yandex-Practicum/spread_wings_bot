import enum


class LegalQuestions(str, enum.Enum):
    """Выбор юридического вопроса из списка."""

    FIRST_QUESTION = "[Заглушка]Первый юридический вопрос"
    SECOND_QUESTION = "[Заглушка]Второй юридический вопрос"
    THIRD_QUESTION = "[Заглушка]Третий юридический вопрос"
