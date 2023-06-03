import enum


class ContactValidate(str, enum.Enum):
    """Валидаторы для контактов."""

    PHONE = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    EMAIL = r"^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$"
