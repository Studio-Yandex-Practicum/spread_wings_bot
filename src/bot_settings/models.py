from django.core.validators import URLValidator
from django.db import models


class BotSettings(models.Model):
    """Model for bot settings."""

    URL = "url"
    TEXT = "text"
    __VALUE_TYPES = (
        (URL, "URL"),
        (TEXT, "TEXT"),
    )
    key = models.CharField(
        max_length=31,
        verbose_name="Ключ настройки",
        primary_key=True,
    )
    title = models.CharField(max_length=255, verbose_name="Название настройки")
    value = models.CharField(max_length=255, verbose_name="Значение настройки")
    type = models.CharField(
        max_length=31,
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
