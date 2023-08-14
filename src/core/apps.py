from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Base configuration for Core app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Регионы"
