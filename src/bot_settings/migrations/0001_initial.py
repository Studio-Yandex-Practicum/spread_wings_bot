# Generated by Django 4.2.4 on 2023-09-07 07:14

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migrations for bot."""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BotSettings",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "key",
                    models.CharField(
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Ключ настройки",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите название настройки для бота",
                        max_length=255,
                        verbose_name="Название настройки",
                    ),
                ),
                (
                    "value",
                    ckeditor.fields.RichTextField(
                        help_text="Введите значение настройки для бота",
                        max_length=255,
                        verbose_name="Значение настройки",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("url", "Ссылка"),
                            ("text", "Текст"),
                            ("int", "Число"),
                        ],
                        max_length=100,
                        verbose_name="Тип значения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Настройка бота",
                "verbose_name_plural": "Настройки бота",
                "ordering": ("title",),
            },
        ),
    ]
