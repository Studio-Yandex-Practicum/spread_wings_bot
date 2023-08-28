# Generated by Django 4.2.4 on 2023-08-28 14:05

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration for fields in Question, FundProgram."""

    dependencies = [
        ("bot", "0003_alter_fundprogram_fund_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fundprogram",
            name="fund_text",
            field=ckeditor.fields.RichTextField(
                help_text="Введите описание программы, не больше 3896 символов",
                max_length=3896,
                verbose_name="Описание программы",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="short_description",
            field=models.CharField(
                help_text="Введите текст для кнопки в боте",
                max_length=20,
                verbose_name="Короткое описание",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="title",
            field=models.CharField(
                help_text="Введите название программы фонда, не больше 200 символов",
                max_length=200,
                unique=True,
                verbose_name="Название",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer",
            field=ckeditor.fields.RichTextField(
                help_text="Введите ответ на вопрос, не больше 3896 символов",
                max_length=3896,
                verbose_name="Ответ",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="question",
            field=models.CharField(
                help_text="Введите вопрос, не больше 200 символов",
                max_length=200,
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="short_description",
            field=models.CharField(
                help_text="Введите текст для кнопки в боте",
                max_length=20,
                verbose_name="Короткое описание",
            ),
        ),
    ]
