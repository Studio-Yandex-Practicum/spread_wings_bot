import asyncio
import logging
from typing import Self
from warnings import filterwarnings

from django.conf import settings
from redis.asyncio import Redis
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)
from telegram.warnings import PTBUserWarning

from .constants.patterns import CONTACT_TYPE_PATTERN, HELP_TYPE_PATTERN
from .constants.regions import Regions
from .constants.states.ask_question_states import AskQuestionStates
from .constants.states.main_states import PATTERN, States
from .handlers.ask_question import (
    get_contact,
    get_name,
    get_question,
    select_contact_type,
)
from .handlers.assistance import (
    ask_question,
    contact_with_us,
    fund_programs,
    receive_assistance,
    select_type_of_help,
    selected_type_assistance,
    show_contact,
)
from .handlers.back_handler import back_button
from .handlers.main_handlers import help_handler, start_handler
from .handlers.service_handlers import (
    answer_all_messages_handler,
    menu_handler,
)
from .persistence import RedisPersistence

logger = logging.getLogger("bot")


class Bot:
    """Interface for Telegram bot library. Implements Singleton pattern."""

    _instance: Self | None = None

    def __new__(cls):
        """Singleton pattern implementation."""
        if not cls._instance:
            cls._instance = super(Bot, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Create the bot instance."""
        self._app = build_app()
        self._stop_event = asyncio.Event()

    def start(self) -> None:
        """Start the bot. It will check for updates until the stop() method is called."""
        logger.info("Bot starting...")
        self._stop_event.clear()
        asyncio.ensure_future(self._run(), loop=asyncio.get_event_loop())

    def stop(self) -> None:
        """Set the stop event to stop the bot."""
        logger.info("Bot stopping...")
        self._stop_event.set()

    async def _run(self) -> None:
        async with self._app:
            await self._app.start()
            if not settings.WEBHOOK_ENABLED:
                await self._app.bot.delete_webhook()
                await self._app.updater.start_polling()
                logger.info("Polling started")
            else:
                await self._app.bot.set_webhook(
                    url=settings.WEBHOOK_URL,
                    secret_token=settings.WEBHOOK_SECRET_KEY,
                    allowed_updates=["message", "callback_query"],
                )
                logger.info(f"Webhook set up at {settings.WEBHOOK_URL}")

            await self._stop_event.wait()

            await self._app.updater.stop()
            await self._app.stop()

    async def process_update(self, data: dict) -> None:
        """Process the update from Telegram. Manual call."""
        await self._app.update_queue.put(Update.de_json(data, self._app.bot))

    @classmethod
    def get_instance(cls) -> Self:
        """Get the bot instance or raise an exception if it is not initialized."""
        if cls._instance is None:
            raise RuntimeError("Bot is not initialized")
        return cls._instance


def build_app() -> Application:
    """Application launch point."""
    logger.info("Building the application...")
    filterwarnings(
        action="ignore",
        message=r".*CallbackQueryHandler",
        category=PTBUserWarning,
    )
    ask_question_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(r"^[^\/].*$"), get_question),
        ],
        persistent=True,
        name="ask_question_handler",
        states={
            AskQuestionStates.QUESTION: [
                MessageHandler(filters.Regex(r"^[^\/].*$"), get_name),
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
                    get_question,
                    pattern=PATTERN.format(state=States.ASK_QUESTION.value),
                )
            ],
        },
        fallbacks=[start_handler],
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
                    contact_with_us,
                    pattern=PATTERN.format(state=States.CONTACT_US.value),
                ),
            ],
            States.QUESTIONS_AND_CONTACTS: [
                CallbackQueryHandler(
                    ask_question,
                    pattern=PATTERN.format(state=States.ASK_QUESTION.value),
                ),
            ],
            States.CONTACT_US: [
                CallbackQueryHandler(
                    show_contact,
                    pattern=PATTERN.format(state=States.SHOW_CONTACT.value),
                ),
                CallbackQueryHandler(
                    ask_question,
                    pattern=PATTERN.format(state=States.ASK_QUESTION.value),
                ),
            ],
            States.SHOW_CONTACT: [
                CallbackQueryHandler(
                    show_contact,
                    pattern=PATTERN.format(state=States.SHOW_CONTACT.value),
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

    if settings.USE_REDIS_PERSISTENCE:
        redis_instance = Redis(
            host=settings.REDIS["host"],
            port=settings.REDIS["port"],
            decode_responses=True,
        )
        persistence = RedisPersistence(redis_instance)
        logger.info("Redis persistence ENABLE")
    else:
        persistence = PicklePersistence(filepath="local_persistence")
        logger.info("Redis persistence DISABLE")

    app = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_TOKEN)
        .persistence(persistence)
        .build()
    )
    app.add_handlers(
        [main_handler, help_handler, menu_handler, answer_all_messages_handler]
    )
    return app
