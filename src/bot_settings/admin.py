from django.contrib import admin

from bot_settings.models import BotSettings


@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    """Base admin configuration for BotSettings model."""

    list_display = ("get_title", "get_type", "get_value", "get_key")
    list_filter = ("title", "type", "value")
    search_fields = ("title", "type", "value", "key")
    readonly_fields = ("key", "type")

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission for BotSettings model."""
        return False

    @admin.display(description="Название настройки")
    def get_title(self, obj):
        """Display title of settings in admin panel."""
        return obj.title[:100]

    @admin.display(description="Тип значения")
    def get_type(self, obj):
        """Display type of settings in admin panel."""
        return obj.type[:100]

    @admin.display(description="Значение настройки")
    def get_value(self, obj):
        """Display value of settings in admin panel."""
        return obj.value[:100]

    @admin.display(description="Ключ настройки")
    def get_key(self, obj):
        """Display key of settings in admin panel."""
        return obj.key[:100]
