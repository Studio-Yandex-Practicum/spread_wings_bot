from django.contrib import admin

from bot_settings.models import BotSettings


@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    """Base admin configuration for BotSettings model."""

    list_display = ("get_title", "type", "get_value")
    list_filter = ("title", "type", "value")
    search_fields = ("title", "type", "value")
    readonly_fields = ("type",)
    exclude = ("key",)

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission for BotSettings model."""
        return False

    @admin.display(description="Название настройки")
    def get_title(self, obj):
        """Display title of settings in admin panel."""
        return obj.title[:100]

    @admin.display(description="Значение настройки")
    def get_value(self, obj):
        """Display value of settings in admin panel."""
        return obj.value[:100]
