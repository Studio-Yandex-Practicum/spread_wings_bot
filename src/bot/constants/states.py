import enum


PATTERN = "^{state}$"


class States(str, enum.Enum):
    """Состояния бота."""

    ASSISTANCE = "assistance"  # п.с. "Помочь или получить помощь"
    REGION = "region"  # п.с. "Выбор региона"
    BACK = "back"
