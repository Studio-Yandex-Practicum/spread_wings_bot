# Generated by Django 4.2.3 on 2023-07-21 08:19
from django.db import migrations

from bot_settings.models import BotSettings as BotSettingsModel


def create_help_message_setting(apps, schema_editor):
    """Create help_message setting instance."""
    BotSettings = apps.get_model("bot_settings", "BotSettings")
    BotSettings.objects.create(
        key="help_message",
        title="Сообщение при нажатии на кнопку Help",
        type=BotSettingsModel.TEXT,
        value="Здесь выводится краткое описание возможностей бота (/help)",
    )


def remove_help_message_setting(apps, schema_editor):
    """Remove help_message setting instance."""
    BotSettings = apps.get_model("bot_settings", "BotSettings")
    setting = BotSettings.objects.get(key="help_message")
    setting.delete()


class Migration(migrations.Migration):
    """Initial migration for bot_settings app."""

    dependencies = [
        ("bot_settings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_help_message_setting,
            reverse_code=remove_help_message_setting,
        ),
    ]
