class InvalidRecipientEmailAddress(Exception):
    """Кастомный эксепшн для поднятия при невалидном адресате."""

    pass


class PostNotFound(Exception):
    """Кастомный эксепшн для поднятия при отсутствии мокового поста."""

    pass
