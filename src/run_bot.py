import logging.config

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ConversationHandler,
)

from bot.constants.regions import Regions
from bot.constants.states import PATTERN, States
from bot.core.config import settings
from bot.core.log_config import LOGGING_CONFIG
from bot.handlers.assistance import back_to_start, receive_assistance
from bot.handlers.assistance_types import (
    back_to_region,
    fund_programs,
    legal_assistance,
    psychological_assistance,
    select_type_of_help,
    social_assistance,
)
from bot.handlers.main_handlers import help_handler, start_handler
from bot.handlers.service_handlers import menu_handler


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
                    pattern=PATTERN.format(state=States.ASSISTANCE.value),
                ),
            ],
            States.REGION: [
                CallbackQueryHandler(
                    select_type_of_help,
                    pattern=PATTERN.format(state=region.name),
                )
                for region in Regions
            ],
            States.ASSISTANCE_TYPE: [
                CallbackQueryHandler(
                    legal_assistance,
                    pattern=PATTERN.format(
                        state=States.LEGAL_ASSISTANCE.value
                    ),
                ),
                CallbackQueryHandler(
                    social_assistance,
                    pattern=PATTERN.format(
                        state=States.SOCIAL_ASSISTANCE.value
                    ),
                ),
                CallbackQueryHandler(
                    psychological_assistance,
                    pattern=PATTERN.format(
                        state=States.PSYCHOLOGICAL_ASSISTANCE.value
                    ),
                ),
                CallbackQueryHandler(
                    fund_programs,
                    pattern=PATTERN.format(state=States.FUND_PROGRAMS.value),
                ),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(
                back_to_start, pattern=PATTERN.format(state=States.BACK.value)
            ),
            CallbackQueryHandler(
                back_to_region,
                pattern=PATTERN.format(state=States.BACK_TO_REGION.value),
            ),
            start_handler,
        ],
    )
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handlers([main_handler, help_handler, menu_handler])
    app.run_polling()


if __name__ == "__main__":
    main()
