# Generated by Django 4.2.3 on 2023-08-01 11:24

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_region_region_key"),
        ("bot", "0004_question_question_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coordinator",
            options={
                "ordering": ("last_name",),
                "verbose_name": "Координатор",
                "verbose_name_plural": "Координаторы",
            },
        ),
        migrations.AlterModelOptions(
            name="fundprogram",
            options={
                "ordering": ("title",),
                "verbose_name": "Программа фонда",
                "verbose_name_plural": "Программы фонда",
            },
        ),
        migrations.AlterModelOptions(
            name="question",
            options={
                "ordering": ("question",),
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="email_address",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="Email"
            ),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="first_name",
            field=models.CharField(max_length=200, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="last_name",
            field=models.CharField(max_length=200, verbose_name="Фамилия"),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=20,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$"
                    )
                ],
                verbose_name="Номер телефона",
            ),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="region",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="coordinators",
                to="core.region",
                verbose_name="Регион",
            ),
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="telegram_account",
            field=models.CharField(
                blank=True,
                max_length=32,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^[\\w\\_]{5,32}$"
                    )
                ],
                verbose_name="Telegram",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="description",
            field=models.CharField(max_length=500, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="regions",
            field=models.ManyToManyField(
                blank=True,
                related_name="programs",
                to="core.region",
                verbose_name="Регионы",
            ),
        ),
        migrations.AlterField(
            model_name="fundprogram",
            name="title",
            field=models.CharField(
                max_length=200, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer",
            field=models.CharField(max_length=3856, verbose_name="Ответ"),
        ),
        migrations.AlterField(
            model_name="question",
            name="question",
            field=models.CharField(max_length=200, verbose_name="Вопрос"),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_type",
            field=models.CharField(
                choices=[
                    ("law", "Юридическая помощь"),
                    ("social", "Социальная помощь"),
                    ("mental", "Психологическая помощь"),
                ],
                default="law",
                max_length=100,
                verbose_name="Тип вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="regions",
            field=models.ManyToManyField(
                blank=True,
                related_name="questions",
                to="core.region",
                verbose_name="Регионы",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="short_description",
            field=models.CharField(
                max_length=20, verbose_name="Короткое описание"
            ),
        ),
    ]
