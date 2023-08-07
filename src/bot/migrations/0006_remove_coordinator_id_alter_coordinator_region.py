# Generated by Django 4.2.3 on 2023-08-07 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_region_options"),
        ("bot", "0005_alter_coordinator_options_alter_fundprogram_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coordinator",
            name="id",
        ),
        migrations.AlterField(
            model_name="coordinator",
            name="region",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                primary_key=True,
                related_name="coordinators",
                serialize=False,
                to="core.region",
                verbose_name="Регион",
            ),
        ),
    ]
