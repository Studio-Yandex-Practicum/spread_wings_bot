from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_startup, asgi_shutdown

from .bot import Bot


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"
    bot = Bot()

    def on_startup(self, **kwargs):
        self.bot.start()

    def on_shutdown(self, **kwargs):
        self.bot.stop()

    def ready(self):
        asgi_startup.connect(self.on_startup)
        asgi_shutdown.connect(self.on_shutdown)
