import re
from typing import Optional

from phonenumbers import PhoneNumberFormat, format_number, is_valid_number
from pydantic import BaseModel, EmailStr, Extra, PositiveInt, validator


class Coordinator(BaseModel):
    """Модель координаторов благотворительного фонда."""

    full_name: str
    region: str
    phone: PositiveInt
    email: EmailStr
    telegram: Optional[str]

    class Config:
        """Файлы конфигурации."""

        extra = Extra.ignore

    @validator("full_name")
    def validate_name(cls, value):
        """Валидация имени координатора."""
        if value is None:
            raise ValueError("Имя не может быть пустым!")
        return value

    @validator("region")
    def validate_region(cls, value):
        """Валидация региона координатора."""
        if value is None:
            raise ValueError("Регион не может быть пустым!")
        return value

    @validator("phone")
    def validate_phone(cls, value):
        """Валидация номера телефона координатора."""
        if value is None:
            raise ValueError("Телефон не может быть пустым!")
        if is_valid_number(value):
            raise ValueError("Телефон не правильный")
        return format_number(value, PhoneNumberFormat.INTERNATIONAL)

    @validator("email")
    def validate_email(cls, value):
        """Валидация электронной почты координатора."""
        if value is None:
            raise ValueError("электронная почта не может быть пустым!")
        if not bool(re.fullmatch(r"[\w.-]+@[\w-]+\.[\w.]+", value)):
            raise ValueError("Электронная почта не правильная")
        return value
