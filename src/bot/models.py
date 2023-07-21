from django.db import models

from core.models import BaseModel, Region
from bot.validators import phone_regex, telegram_regex


class Coordinator(BaseModel):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    region = models.ForeignKey(Region,
                               on_delete=models.PROTECT,
                               null=True,
                               related_name='coordinators')
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    validators=[phone_regex],
                                    blank=True)
    telegram_account = models.CharField(max_length=32,
                                        unique=True,
                                        validators=[telegram_regex],
                                        blank=True)


class Question(BaseModel):

    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=3856)
    short_description = models.CharField(max_length=20)
    regions = models.ManyToManyField(Region,
                                     related_name='questions',
                                     blank=True)


class FundProgram(BaseModel):

    title = models.CharField(max_length=200,
                             unique=True)
    description = models.CharField(max_length=500)
    regions = models.ManyToManyField(Region,
                                     related_name='programs',
                                     blank=True)