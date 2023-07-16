import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field, validator

PHONE = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"


class Contacts(BaseModel):
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


class Question(BaseModel):
    """Input data question model."""

    question: str = Field(..., min_length=30)
    name: str = Field(..., min_length=1)
    contact: str
    question_type: str

    class Config:
        """Additional params."""

        orm_mode = True
        extra = Extra.forbid
