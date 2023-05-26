import logging.config

from telegram.ext import (ApplicationBuilder,
                          CallbackQueryHandler,
                          ConversationHandler)

from bot.constants.states import PATTERN, States, HELP, GET_HELP, BACK
from bot.core.config import settings
from bot.core.log_config import LOGGING_CONFIG
from bot.handlers.assistance import (back_to_start,
                                     make_donation,
                                     receive_assistance)
from bot.handlers.main_handlers import start_handler


def main():
    """Application launch point."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bot")
    logger.info("start")
    main_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            States.ASSISTANCE: [
                CallbackQueryHandler(
                    receive_assistance,
                    pattern=PATTERN.format(state=GET_HELP)
                ),
                CallbackQueryHandler(
                    make_donation,
                    pattern=PATTERN.format(state=HELP)
                )
            ]
        },
        # TODO в дальнейшем думаю надо добавить stop_handler для fallbacks
        fallbacks=[
            CallbackQueryHandler(
                back_to_start,
                pattern=PATTERN.format(state=BACK)
            ),
            start_handler,
        ],
    )
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handler(main_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
