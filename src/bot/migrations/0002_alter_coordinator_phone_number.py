# Generated by Django 4.2.4 on 2023-08-24 15:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coordinator",
            name="phone_number",
            field=models.CharField(
                blank=True,
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
    ]
