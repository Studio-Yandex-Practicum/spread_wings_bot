from django.contrib import admin

from bot_settings.models import BotSettings


@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    """Base admin configuration for BotSettings model."""

    list_filter = ("type",)
    search_fields = ("title", "type", "value")
    readonly_fields = ("type",)
    exclude = ("key", "title")

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission for BotSettings model."""
        return False
