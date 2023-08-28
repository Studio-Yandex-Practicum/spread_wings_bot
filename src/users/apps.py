from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Base configuration for Users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"

    def ready(self):
        """Import User model signals."""
        import users.signals  # noqa
