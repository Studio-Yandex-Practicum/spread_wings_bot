from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_shutdown

from bot import Bot


class BotConfig(AppConfig):
    """Base Django application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"
    bot: Bot

    def on_shutdown(self, **kwargs):
        """Call when the app is shutting down."""
        self.bot.stop()

    def ready(self):
        """Call when the app has been started."""
        asgi_shutdown.connect(self.on_shutdown)
        self.bot = Bot()
        self.bot.start()
