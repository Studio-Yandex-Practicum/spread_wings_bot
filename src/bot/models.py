from django.db import models

from core.models import BaseModel, Region
from bot.validators import (phone_regex,
                            telegram_regex,
                            format_phone_number,
                            format_telegram_link)


class Coordinator(BaseModel):

    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    region = models.OneToOneField(Region,
                                  on_delete=models.PROTECT,
                                  primary_key=True,
                                  related_name='coordinators',
                                  verbose_name='Регион')
    email_address = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20,
                                    unique=True,
                                    validators=[phone_regex],
                                    blank=True,
                                    verbose_name='Номер телефона')
    telegram_account = models.CharField(max_length=32,
                                        unique=True,
                                        validators=[telegram_regex],
                                        blank=True,
                                        verbose_name='Telegram')

    def save(self, *args, **kwargs):
        self.telegram_account = format_telegram_link(self.telegram_account)
        self.phone_number = format_phone_number(self.phone_number)
        return super(Coordinator, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Координатор"
        verbose_name_plural = "Координаторы"
        ordering = ("last_name",)


class Question(BaseModel):

    LAW = 'law'
    SOCIAL = 'social'
    MENTAL = 'mental'

    HELP_TYPES = [
        (LAW, 'Юридическая помощь'),
        (SOCIAL, 'Социальная помощь'),
        (MENTAL, 'Психологическая помощь')
    ]

    question = models.CharField(max_length=200, verbose_name="Вопрос")
    answer = models.CharField(max_length=3856, verbose_name="Ответ")
    short_description = models.CharField(max_length=20, verbose_name="Короткое описание")
    regions = models.ManyToManyField(Region,
                                     related_name='questions',
                                     blank=True,
                                     verbose_name='Регионы')
    question_type = models.CharField(
        max_length=100,
        choices=HELP_TYPES,
        default=LAW,
        verbose_name='Тип вопроса'
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ("question",)


class FundProgram(BaseModel):

    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='Название')
    description = models.CharField(max_length=500, verbose_name='Описание')
    regions = models.ManyToManyField(Region,
                                     related_name='programs',
                                     blank=True,
                                     verbose_name='Регионы')

    class Meta:
        verbose_name = "Программа фонда"
        verbose_name_plural = "Программы фонда"
        ordering = ("title",)
