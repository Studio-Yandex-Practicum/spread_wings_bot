from pydantic import BaseModel, EmailStr, Field


class MailValidator(BaseModel):
    """Validator for Mail."""

    subject: str = Field(..., max_length=100)
    message: str = Field(..., max_length=1000)
    recipients: list[EmailStr] = Field(
        ..., min_items=1, max_items=100, unique_items=True
    )
