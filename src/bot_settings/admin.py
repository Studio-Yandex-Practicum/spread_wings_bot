from django.contrib import admin

from bot_settings.models import BotSettings


@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    """Base admin configuration for BotSettings model."""

    list_display = ("title", "type", "value", "key")
    list_filter = ("title", "type", "value")
    search_fields = ("title", "type", "value", "key")
    readonly_fields = ("key", "type")

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission for BotSettings model."""
        return False
