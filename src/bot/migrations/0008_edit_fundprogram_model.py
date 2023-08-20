# Generated by Django 4.2.4 on 2023-08-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):
    """New migrations for database."""

    dependencies = [
        ("core", "0003_alter_region_options"),
        ("bot", "0007_alter_coordinator_phone_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProxyRegion",
            fields=[],
            options={
                "verbose_name": "Регион",
                "verbose_name_plural": "Регионы",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.region",),
        ),
        migrations.RemoveField(
            model_name="fundprogram",
            name="description",
        ),
        migrations.AddField(
            model_name="fundprogram",
            name="fund_text",
            field=models.TextField(
                max_length=4096, verbose_name="Описание программы"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fundprogram",
            name="short_description",
            field=models.CharField(
                default="button",
                max_length=20,
                verbose_name="Короткое описание",
            ),
            preserve_default=False,
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
                max_length=100,
                verbose_name="Тип вопроса",
            ),
        ),
    ]