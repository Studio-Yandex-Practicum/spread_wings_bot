import logging

from telegram.ext import ApplicationBuilder

from bot.core.config import settings
from bot.handlers.main_handlers import help_handler, start_handler
from src.bot.core.logging import config_log


def main():
    config_log()
    logging.info('start')
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handlers([start_handler, help_handler])
    app.run_polling()


if __name__ == '__main__':
    main()
