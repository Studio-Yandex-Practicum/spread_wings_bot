import logging.config
from warnings import filterwarnings

from redis.asyncio import Redis
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)
from telegram.warnings import PTBUserWarning

from bot.constants.patterns import CONTACT_TYPE_PATTERN, HELP_TYPE_PATTERN
from bot.constants.regions import Regions
from bot.constants.states.ask_question_states import AskQuestionStates
from bot.constants.states.main_states import PATTERN, States
from bot.core.config import settings
from bot.core.log_config import LOGGING_CONFIG
from bot.core.redis_persistence import RedisPersistence
from bot.handlers.ask_question import (
    get_contact,
    get_name,
    get_question,
    select_contact_type,
)
from bot.handlers.assistance import (
    ask_question_assistance,
    contact_with_us_assistance,
    receive_assistance,
)
from bot.handlers.assistance_types import (
    contact_with_us,
    fund_programs,
    select_type_of_help,
    selected_type_assistance,
    show_contact,
)
from bot.handlers.back_handler import back_button
from bot.handlers.main_handlers import help_handler, start_handler
from bot.handlers.service_handlers import (
    answer_all_messages_handler,
    menu_handler,
)


def main():
    """Application launch point."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bot")
    filterwarnings(
        action="ignore",
        message=r".*CallbackQueryHandler",
        category=PTBUserWarning,
    )
    logger.info("start")
    ask_question_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^.*$"), get_question),
        ],
        persistent=True,
        name="ask_question_handler",
        states={
            AskQuestionStates.QUESTION: [
                MessageHandler(filters.Regex("^.*$"), get_name),
            ],
            AskQuestionStates.NAME: [
                CallbackQueryHandler(
                    get_name,
                    pattern=PATTERN.format(
                        state=AskQuestionStates.CONTACT_TYPE.value
                    ),
                ),
            ],
            AskQuestionStates.CONTACT_TYPE: [
                CallbackQueryHandler(
                    select_contact_type, pattern=CONTACT_TYPE_PATTERN
                )
            ],
            AskQuestionStates.ENTER_YOUR_CONTACT: [
                MessageHandler(filters.Regex(r"^[^\/].*$"), get_contact)
            ],
            States.ASK_QUESTION: [
                CallbackQueryHandler(
                    ask_question_assistance,
                    pattern=PATTERN.format(state=States.ASK_QUESTION.value),
                )
            ],
        },
        fallbacks=[],
        map_to_parent={
            AskQuestionStates.END: States.ASSISTANCE,
            States.ASSISTANCE: States.ASSISTANCE,
        },
    )
    logger.info("ask_question_handler deploy")
    main_handler = ConversationHandler(
        entry_points=[start_handler],
        persistent=True,
        name="main_handler",
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
                    selected_type_assistance,
                    pattern=HELP_TYPE_PATTERN,
                ),
                CallbackQueryHandler(
                    fund_programs,
                    pattern=PATTERN.format(state=States.FUND_PROGRAMS.value),
                ),
                CallbackQueryHandler(
                    contact_with_us_assistance,
                    pattern=PATTERN.format(state=States.CONTACT_US.value),
                ),
            ],
            States.CONTACT_US: [
                CallbackQueryHandler(
                    contact_with_us,
                    pattern=PATTERN.format(state=States.CONTACT_US.value),
                )
            ],
            States.SHOW_CONTACT: [
                CallbackQueryHandler(
                    show_contact,
                    pattern=PATTERN.format(state=States.SHOW_CONTACT.value),
                )
            ],
            States.SELECTED_TYPE: [
                CallbackQueryHandler(
                    ask_question_assistance,
                    pattern=PATTERN.format(state=States.ASK_QUESTION.value),
                )
            ],
            States.ASK_QUESTION: [ask_question_handler],
        },
        fallbacks=[
            CallbackQueryHandler(
                back_button,
                pattern=r"back_to_",
            ),
            start_handler,
        ],
    )
    logger.info("main_handler deploy")

    if settings.redis:
        redis_instance = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
        )
        persistence = RedisPersistence(redis_instance)
        logger.info("Redis persistence ENABLE")
    else:
        persistence = PicklePersistence(filepath="local_persistence")
        logger.info("Redis persistence DISABLE")

    app = (
        ApplicationBuilder()
        .token(settings.telegram_token.get_secret_value())
        .persistence(persistence)
        .build()
    )
    app.add_handlers(
        [main_handler, help_handler, menu_handler, answer_all_messages_handler]
    )
    app.run_polling()


if __name__ == "__main__":
    main()
