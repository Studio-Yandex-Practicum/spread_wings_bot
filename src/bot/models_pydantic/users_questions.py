import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field, validator

from bot.validators import EMAIL, PHONE

EMAIL_VALUE_ERROR = "Неправильно указана электронная почта: {email}"
PHONE_NUMBER_VALUE_ERROR = "Неправильно указан номер телефона: {phone_number}"
TYPE_QUESTION_TYPES = {
    "LEGAL_ASSISTANCE": "Юридическая помощь",
    "SOCIAL_ASSISTANCE": "Социальная помощь",
    "PSYCHOLOGICAL_ASSISTANCE": "Психологическая помощь",
    "COMMON_QUESTION": "Общий вопрос",
}


class UserContacts(BaseModel):
    """Contact model for validation."""

    email: Optional[EmailStr]
    phone: Optional[str]

    @validator("phone")
    def phone_validation(cls, phone):
        """Phone field validator."""
        if phone and not re.match(PHONE, phone):
            raise ValueError(
                PHONE_NUMBER_VALUE_ERROR.format(phone_number=phone)
            )
        return phone

    @validator("email")
    def email_validator(cls, email):
        """Email field validator."""
        if email and not re.match(EMAIL, email):
            raise ValueError(EMAIL_VALUE_ERROR.format(email=email))
        return email

    class Config:
        """Additional params."""

        orm_mode = True


class UserQuestion(BaseModel):
    """Input data question model."""

    question: str = Field(..., min_length=5)
    name: str = Field(..., min_length=1)
    contact: str
    question_type: str

    def to_representation(self):
        """Representation data."""
        return (
            f"Пользователь: {self.name}\n"
            f"Контакт: {self.contact}\n"
            f"Тема вопроса: {TYPE_QUESTION_TYPES[self.question_type]}\n"
            f"Вопрос: {self.question}"
        )

    class Config:
        """Additional params."""

        orm_mode = True
        extra = Extra.forbid
