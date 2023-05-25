from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ConversationHandler

from bot.constants import ASSISTANCE, DONATION
from bot.core.config import settings
from bot.handlers.assistance import make_donation, receive_assistance
import logging.config

from bot.core.log_config import LOGGING_CONFIG
from bot.handlers.main_handlers import help_handler, start_handler


def main():
    """Application launch point."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bot")
    logger.info("start")
    main_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            ASSISTANCE: [
                CallbackQueryHandler(
                    receive_assistance,
                    pattern=f'^{ASSISTANCE}$'
                ),
                CallbackQueryHandler(make_donation, pattern=f'^{DONATION}$')
            ]
        },
        fallbacks=[
            start_handler,
        ],
    )
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handlers([main_handler, help_handler])
    app.run_polling()


if __name__ == "__main__":
    main()
