from ckeditor.fields import RichTextField
from django.core.validators import URLValidator
from django.db import models

from core.models import BaseModel


class BotSettings(BaseModel):
    """Model for bot settings."""

    URL = "url"
    TEXT = "text"
    INT = "int"
    __VALUE_TYPES = ((URL, "URL"), (TEXT, "TEXT"), (INT, "INT"))
    key = models.CharField(
        max_length=100,
        verbose_name="Ключ настройки",
        primary_key=True,
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название настройки",
        help_text="Введите название настройки для бота",
    )
    value = RichTextField(
        max_length=255,
        verbose_name="Значение настройки",
        help_text="Введите значение настройки для бота",
    )
    type = models.CharField(
        max_length=100,
        verbose_name="Тип значения",
        choices=__VALUE_TYPES,
    )

    def clean(self):
        """Validate value field."""
        if self.type == self.URL:
            URLValidator()(self.value)

    def __str__(self):
        return f"<BotSettings:  {self.key} - {self.title} - {self.value}>"

    class Meta:
        """Meta for BotSettings model."""

        verbose_name = "Настройка бота"
        verbose_name_plural = "Настройки бота"
        ordering = ("title",)
