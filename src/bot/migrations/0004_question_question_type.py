# Generated by Django 4.2.3 on 2023-07-31 13:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0003_alter_coordinator_phone_number"),
    ]

    operations = [
        migrations.AddField(
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
            ),
        ),
    ]
