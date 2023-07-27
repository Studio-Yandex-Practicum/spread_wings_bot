from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_shutdown


class BotConfig(AppConfig):
    """Base Django application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def on_shutdown(self, **kwargs):
        """Call when the app is shutting down."""
        self.bot.stop()

    def ready(self):
        """Call when the app has been started."""
        from bot.bot import Bot

        self.bot = Bot()

        asgi_shutdown.connect(self.on_shutdown)
        self.bot.start()
