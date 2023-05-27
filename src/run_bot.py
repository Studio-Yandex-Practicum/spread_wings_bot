import logging.config

from telegram.ext import (ApplicationBuilder, 
                          CallbackQueryHandler,
                          ConversationHandler)

from bot.constants.states import States
from bot.core.config import settings
from bot.core.log_config import LOGGING_CONFIG
from bot.handlers.assistance import make_donation, choose_region
from bot.handlers.main_handlers import help_handler, start_handler


def main():
    """Application launch point."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bot")
    logger.info("start")
    main_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            States.ASSISTANCE: [
                CallbackQueryHandler(make_donation, pattern=States.DONATION),
                CallbackQueryHandler(choose_region, pattern=States.REGION)     
            ],
            States.DONATION: [
                CallbackQueryHandler(make_donation)
            ],
            States.REGION: [
                CallbackQueryHandler(choose_region)
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
