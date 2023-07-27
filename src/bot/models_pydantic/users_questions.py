import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field, validator

from bot.validators import PHONE


class UserContacts(BaseModel):
    """Contact model for validation."""

    email: Optional[EmailStr]
    phone: Optional[str]

    @validator("phone")
    def phone_validation(cls, phone):
        """Phone field validator."""
        if phone and not re.match(PHONE, phone):
            raise ValueError()
        return phone

    class Config:
        """Additional params."""

        orm_mode = True


class UserQuestion(BaseModel):
    """Input data question model."""

    question: str = Field(..., min_length=30)
    name: str = Field(..., min_length=1)
    contact: str
    question_type: str

    def to_representation(self):
        return (
            f"Пользователь {self.name} (контакт: {self.contact})\n"
            f"Тема вопроса: {self.question_type}\n"
            f"Вопрос: {self.question}"
        )

    class Config:
        """Additional params."""

        orm_mode = True
        extra = Extra.forbid
