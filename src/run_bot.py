import logging.config
import asyncio
from telegram import MenuButton, MenuButtonDefault
from telegram.ext import (ApplicationBuilder,
                          CallbackQueryHandler,
                          ConversationHandler)

from bot.constants.states import PATTERN, States
from bot.core.config import settings
from bot.core.log_config import LOGGING_CONFIG
from bot.handlers.assistance import (back_to_start,
                                     choose_region,
                                     make_donation,
                                     receive_assistance)
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
                CallbackQueryHandler(
                    receive_assistance,
                    pattern=PATTERN.format(state=States.ASSISTANCE.value)
                ),
                CallbackQueryHandler(
                    make_donation,
                    pattern=PATTERN.format(state=States.DONATION.value)
                ),
                CallbackQueryHandler(
                    choose_region,
                    pattern=PATTERN.format(state=States.REGION.value)
                )
            ]
        },
        # TODO в дальнейшем думаю надо добавить stop_handler для fallbacks
        fallbacks=[
            CallbackQueryHandler(
                back_to_start,
                pattern=PATTERN.format(state=States.BACK.value)
            ),
            start_handler,
        ],
    )
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handlers([main_handler, help_handler])
    # app.run_polling()
    # menu_button = MenuButton({"start" : "/start"})
    # menu_button_default = MenuButtonDefault(start="/start")
    # app.create_task(app.bot.set_chat_menu_button(menu_button=menu_button))
    app.run_polling()
    return app


if __name__ == "__main__":
    app = main()
    loop = asyncio.get_event_loop()
    menu_button = MenuButton({"start" : "/start"})
    menu_task = app.create_task(app.bot.set_chat_menu_button(menu_button=menu_button))
    loop.run_until_complete(asyncio.wait(menu_task))
    loop.close()
