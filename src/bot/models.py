from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from bot.validators import (
    format_phone_number,
    format_telegram_link,
    phone_regex,
    telegram_regex,
    validate_is_chief,
)
from core.models import BaseModel, Region


class Coordinator(BaseModel):
    """Region coordinator model."""

    first_name = models.CharField(
        max_length=200,
        verbose_name="Имя",
        help_text="Введите имя регионального координатора",
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name="Фамилия",
        help_text="Введите фамилию регионального координатора",
    )
    region = models.OneToOneField(
        Region,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="coordinators",
        verbose_name="Регион",
        help_text="Выберите регион из списка",
    )
    email_address = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите адрес электронной почты",
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_regex],
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона регионального координатора",
    )
    telegram_account = models.CharField(
        max_length=32,
        unique=True,
        validators=[telegram_regex],
        blank=True,
        null=True,
        verbose_name="Telegram",
        help_text="Введите телеграмм-аккаунт регионального координатора",
    )
    is_chief = models.BooleanField(
        default=False, validators=[validate_is_chief], verbose_name="Главный"
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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Координатор"
        verbose_name_plural = "Координаторы"
        ordering = (
            "-is_chief",
            "last_name",
        )


class HelpTypes(models.TextChoices):
    """Supporting model to make choices field."""

    LEGAL_ASSISTANCE = "LEGAL_ASSISTANCE", _("Юридическая помощь")
    SOCIAL_ASSISTANCE = "SOCIAL_ASSISTANCE", _("Социальная помощь")
    PSYCHOLOGICAL_ASSISTANCE = "PSYCHOLOGICAL_ASSISTANCE", _(
        "Психологическая помощь"
    )


class Question(BaseModel):
    """Assistance question model."""

    question = models.CharField(
        max_length=200,
        verbose_name="Вопрос",
        help_text="Введите вопрос, не более 200 символов",
    )
    answer = RichTextField(
        max_length=3896,
        verbose_name="Ответ",
        help_text="Введите ответ на вопрос, не более 3896 символов",
    )
    short_description = models.CharField(
        max_length=20,
        verbose_name="Текст на кнопке",
        help_text="Введите название кнопки в боте для данного вопроса",
    )
    regions = models.ManyToManyField(
        Region,
        related_name="questions",
        blank=True,
        verbose_name="Регионы",
        help_text="Выберите регион(ы) для вопроса",
    )
    question_type = models.CharField(
        max_length=100,
        choices=HelpTypes.choices,
        default=HelpTypes.LEGAL_ASSISTANCE,
        verbose_name="Тип вопроса",
        help_text="Выберите тип помощи для вопроса",
    )

    def __str__(self):
        return self.short_description

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ("question",)


class FundProgram(BaseModel):
    """Fund program model."""

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
        help_text="Введите название программы фонда, не более 200 символов",
    )
    fund_text = RichTextField(
        max_length=3896,
        verbose_name="Описание программы",
        help_text="Введите описание программы, не более 3896 символов",
    )
    short_description = models.CharField(
        max_length=20,
        verbose_name="Текст на кнопке",
        help_text="Введите название кнопки в боте для данной программы",
    )
    regions = models.ManyToManyField(
        Region,
        related_name="programs",
        blank=True,
        verbose_name="Регионы",
        help_text="Выберите регион(ы) для программы",
    )

    def __str__(self):
        return self.short_description

    class Meta:
        verbose_name = "Программа фонда"
        verbose_name_plural = "Программы фонда"
        ordering = ("title",)


class ProxyRegion(Region):
    """ProxyRegion model."""

    class Meta:
        proxy = True
        verbose_name_plural = "Регионы"
        verbose_name = "Регион"
