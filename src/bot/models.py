from django.db import models
from django.utils.translation import gettext_lazy as _

from bot.validators import (
    format_phone_number,
    format_telegram_link,
    phone_regex,
    telegram_regex,
)
from core.models import BaseModel, Region


class Coordinator(BaseModel):
    """Region coordinator model."""

    first_name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name="Фамилия",
    )
    region = models.OneToOneField(
        Region,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="coordinators",
        verbose_name="Регион",
    )
    email_address = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_regex],
        blank=True,
        null=True,
        verbose_name="Номер телефона",
    )
    telegram_account = models.CharField(
        max_length=32,
        unique=True,
        validators=[telegram_regex],
        blank=True,
        null=True,
        verbose_name="Telegram",
    )

    def save(self, *args, **kwargs):
        """Check and save telegram_account and phone_number."""
        if self.telegram_account is not None:
            self.telegram_account = format_telegram_link(self.telegram_account)
        if self.phone_number is not None:
            self.phone_number = format_phone_number(self.phone_number)
        return super(Coordinator, self).save(*args, **kwargs)

    def __repr__(self):
        representation = (
            f"ФИО Координатора:"
            f" {self.first_name} {self.last_name}\n"
            f"Email: {self.email_address}\n"
        )
        if self.phone_number is not None:
            representation += f"Телефон: {self.phone_number}\n"
        if self.telegram_account is not None:
            representation += f"Telegram: {self.telegram_account}"
        return representation

    class Meta:  # noqa
        verbose_name = "Координатор"
        verbose_name_plural = "Координаторы"
        ordering = ("last_name",)


class HelpTypes(models.TextChoices):
    """Supporting model to make choices field."""

    LEGAL_ASSISTANCE = "LEGAL_ASSISTANCE", _("Юридическая помощь")
    SOCIAL_ASSISTANCE = "SOCIAL_ASSISTANCE", _("Социальная помощь")
    PSYCHOLOGICAL_ASSISTANCE = "PSYCHOLOGICAL_ASSISTANCE", _(
        "Психологическая помощь"
    )
    COMMON_QUESTION = "COMMON_QUESTION", _("Общий вопрос")


class Question(BaseModel):
    """Assistance question model."""

    question = models.CharField(
        max_length=200,
        verbose_name="Вопрос",
    )
    answer = models.CharField(
        max_length=3856,
        verbose_name="Ответ",
    )
    short_description = models.CharField(
        max_length=20,
        verbose_name="Короткое описание",
    )
    regions = models.ManyToManyField(
        Region,
        related_name="questions",
        blank=True,
        verbose_name="Регионы",
    )
    question_type = models.CharField(
        max_length=100,
        choices=HelpTypes.choices,
        default=HelpTypes.LEGAL_ASSISTANCE,
        verbose_name="Тип вопроса",
    )

    class Meta:  # noqa
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ("question",)


class FundProgram(BaseModel):
    """Fund program model."""

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Описание",
    )
    regions = models.ManyToManyField(
        Region,
        related_name="programs",
        blank=True,
        verbose_name="Регионы",
    )

    class Meta:  # noqa
        verbose_name = "Программа фонда"
        verbose_name_plural = "Программы фонда"
        ordering = ("title",)


class ProxyRegion(Region):
    """ProxyRegion model."""

    class Meta:  # noqa
        proxy = True
        verbose_name_plural = "Регионы"
        verbose_name = "Регион"
