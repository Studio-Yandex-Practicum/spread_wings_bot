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

from bot.constants.patterns import (
    BACK,
    CONTACT,
    CONTACT_US,
    FUND_PROGRAMS,
    GET_ASSISTANCE,
    GET_USER_QUESTION,
    GET_USERNAME,
    HELP_TYPE,
    MESSAGE_PATTERN,
    PATTERN,
    SHOW_CONTACT,
    SHOW_PROGRAM,
    SHOW_QUESTION,
)
from bot.constants.states import States
from bot.handlers.ask_question import (
    get_contact_and_send_email_to_region_coordinator,
    get_question,
    get_username,
    get_username_after_returning_back,
    send_email_to_region_coordinator,
)
from bot.handlers.assistance import (
    contact_with_us,
    fund_programs,
    get_assistance,
    get_user_question,
    select_assistance,
    select_type_of_assistance,
    show_contact,
    show_program,
)
from bot.handlers.back_handler import back_button
from bot.handlers.main_handlers import help_handler, start_handler
from bot.handlers.service_handlers import answer_all_messages_handler
from bot.handlers.show_question import show_question
from bot.persistence import RedisPersistence
from core.models import Region

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
        self._app: Application | None = None
        self._stop_event = asyncio.Event()

    def start(self) -> None:
        """
        Start the bot.

        It will check for updates until the stop() method is called.
        """
        logger.info("Bot starting...")
        self._stop_event.clear()
        asyncio.ensure_future(self._run(), loop=asyncio.get_event_loop())

    def stop(self) -> None:
        """Set the stop event to stop the bot."""
        logger.info("Bot stopping...")
        self._stop_event.set()

    async def _run(self) -> None:
        self._app = await build_app()

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
        """
        Get the bot instance.

        Raise an exception if it is not initialized.
        """
        if cls._instance is None:
            raise RuntimeError("Bot is not initialized")
        return cls._instance


async def build_app() -> Application:
    """Application launch point."""
    logger.info("Building the application...")
    region_keys = [
        key
        async for key in Region.objects.values_list("region_key", flat=True)
    ]
    filterwarnings(
        action="ignore",
        message=r".*CallbackQueryHandler",
        category=PTBUserWarning,
    )
    main_handler = ConversationHandler(
        entry_points=[start_handler],
        persistent=True,
        name="main_handler",
        states={
            States.GET_ASSISTANCE: [
                CallbackQueryHandler(get_assistance, pattern=GET_ASSISTANCE),
            ],
            States.REGION: [
                CallbackQueryHandler(
                    select_type_of_assistance,
                    pattern=PATTERN.format(state=key),
                )
                for key in region_keys
            ],
            States.ASSISTANCE_TYPE: [
                CallbackQueryHandler(select_assistance, pattern=HELP_TYPE),
                CallbackQueryHandler(fund_programs, pattern=FUND_PROGRAMS),
                CallbackQueryHandler(contact_with_us, pattern=CONTACT_US),
                CallbackQueryHandler(
                    get_user_question, pattern=GET_USER_QUESTION
                ),
                CallbackQueryHandler(show_program, pattern=SHOW_PROGRAM),
                CallbackQueryHandler(show_question, pattern=SHOW_QUESTION),
            ],
            States.CONTACT_US: [
                CallbackQueryHandler(show_contact, pattern=SHOW_CONTACT),
                CallbackQueryHandler(
                    get_user_question, pattern=GET_USER_QUESTION
                ),
            ],
            States.SHOW_CONTACT: [
                CallbackQueryHandler(show_contact, pattern=SHOW_CONTACT),
            ],
            States.GET_USER_QUESTION: [
                MessageHandler(filters.Regex(MESSAGE_PATTERN), get_question)
            ],
            States.GET_USERNAME: [
                MessageHandler(filters.Regex(MESSAGE_PATTERN), get_username),
                CallbackQueryHandler(
                    get_username_after_returning_back, pattern=GET_USERNAME
                ),
            ],
            States.SEND_EMAIL: [
                CallbackQueryHandler(
                    send_email_to_region_coordinator, pattern=CONTACT
                ),
            ],
            States.GET_CONTACT: [
                MessageHandler(
                    filters.Regex(MESSAGE_PATTERN),
                    get_contact_and_send_email_to_region_coordinator,
                )
            ],
        },
        fallbacks=[
            CallbackQueryHandler(back_button, pattern=BACK),
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
    app.add_handlers([main_handler, help_handler, answer_all_messages_handler])
    return app
