from django.db import models
from django.core.validators import RegexValidator

from .models.users_questions import PHONE

TELEGRAM_USERNAME = r"^[\w\_]{5,32}$"


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FundRegion(BaseModel):

    region_name = models.CharField(max_length=200, unique=True)


class FundCoordinator(BaseModel):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    region = models.ForeignKey(FundRegion,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='coordinators')
    email_address = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=PHONE)
    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    validators=[phone_regex],
                                    blank=True)
    telegram_regex = RegexValidator(regex=TELEGRAM_USERNAME)
    telegram_account = models.CharField(max_length=32,
                                        unique=True,
                                        validators=[telegram_regex],
                                        blank=True)


class FundQuestion(BaseModel):

    question = models.TextField()
    answer = models.TextField()
    short_description = models.CharField(max_length=200)
    regions = models.ManyToManyField(FundRegion,
                                     related_name='questions',
                                     blank=True)


class FundProgram(BaseModel):

    title = models.CharField(max_length=200,
                             unique=True)
    description = models.TextField()
    regions = models.ManyToManyField(FundRegion,
                                     related_name='programs',
                                     blank=True)