# Generated by Django 4.2.4 on 2023-08-28 21:33

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migrations for bot."""

    dependencies = [
        ("core", "0001_initial"),
        ("bot", "0002_alter_coordinator_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coordinator",
            name="first_name",
            field=models.CharField(
                help_text="Введите имя регионального координатора",
                max_length=200,
                verbose_name="Имя",
            ),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="last_name",
            field=models.CharField(
                help_text="Введите фамилию регионального координатора",
                max_length=200,
                verbose_name="Фамилия",
            ),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="phone_number",
            field=models.CharField(
                blank=True,
                help_text="Введите номер телефона регионального координатора",
                max_length=20,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Введите номер телефона в формате: +7 (777) 777-77-77",
                        regex="^[\\+]?[7, 8][-\\s\\.]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{2}[-\\s\\.]?[0-9]{2}$",
                    )
                ],
                verbose_name="Номер телефона",
            ),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="telegram_account",
            field=models.CharField(
                blank=True,
                help_text="Введите телеграмм-аккаунт регионального координатора",
                max_length=32,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Введите название аккаунта telegram в формате: username",
                        regex="^[\\w\\_]{5,32}$",
                    )
                ],
                verbose_name="Telegram",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="fund_text",
            field=ckeditor.fields.RichTextField(
                help_text="Введите описание программы, не более 3896 символов",
                max_length=3896,
                verbose_name="Описание программы",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="short_description",
            field=models.CharField(
                help_text="Введите название кнопки в боте для данной программы",
                max_length=20,
                verbose_name="Короткое описание",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="title",
            field=models.CharField(
                help_text="Введите название программы фонда, не более 200 символов",
                max_length=200,
                unique=True,
                verbose_name="Название",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer",
            field=ckeditor.fields.RichTextField(
                help_text="Введите ответ на вопрос, не более 3896 символов",
                max_length=3896,
                verbose_name="Ответ",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="question",
            field=models.CharField(
                help_text="Введите вопрос, не более 200 символов",
                max_length=200,
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_type",
            field=models.CharField(
                choices=[
                    ("LEGAL_ASSISTANCE", "Юридическая помощь"),
                    ("SOCIAL_ASSISTANCE", "Социальная помощь"),
                    ("PSYCHOLOGICAL_ASSISTANCE", "Психологическая помощь"),
                    ("COMMON_QUESTION", "Общий вопрос"),
                ],
                default="LEGAL_ASSISTANCE",
                help_text="Выберите тип помощи для вопроса",
                max_length=100,
                verbose_name="Тип вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="regions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Выберите регион(ы) для вопроса",
                related_name="questions",
                to="core.region",
                verbose_name="Регионы",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="short_description",
            field=models.CharField(
                help_text="Введите название кнопки в боте для данного вопроса",
                max_length=20,
                verbose_name="Короткое описание",
            ),
        ),
    ]