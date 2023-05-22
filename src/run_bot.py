from telegram.ext import ApplicationBuilder

from bot.handlers.main_handlers import start_handler, help_handler
from bot.core.config import settings


def main():
    app = ApplicationBuilder().token(settings.token).build()
    app.add_handlers([start_handler, help_handler])
    app.run_polling()


if __name__ == '__main__':
    main()