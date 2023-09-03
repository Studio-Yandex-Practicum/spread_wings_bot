import asyncio
from typing import Any, Awaitable, Callable

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.constants.messages import ANSWER_TO_USER_MESSAGE
from bot.constants.states import States
from bot.handlers.ask_question import get_username_after_returning_back
from bot.handlers.assistance import (
    contact_with_us,
    fund_programs,
    get_assistance,
    get_user_question,
    select_assistance,
    select_type_of_assistance,
)
from bot.handlers.debug_handlers import debug_logger
from bot.handlers.main_handlers import start
from bot.handlers.show_objects import show_contact


@debug_logger(
    state=States.ANSWER_TO_USER_MESSAGE,
    run_functions_debug_loger="answer_all_messages",
)
async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Process any message entered by the user."""
    await update.message.delete()
    message = await update.message.reply_text(ANSWER_TO_USER_MESSAGE)

    await asyncio.sleep(3)
    await context.bot.delete_message(
        chat_id=message.chat_id, message_id=message.message_id
    )


answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)


FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.START: start,
    States.ASSISTANCE_TYPE: select_type_of_assistance,
    States.CONTACT_US: contact_with_us,
    States.FUND_PROGRAMS: fund_programs,
    States.REGION.value: get_assistance,
    States.SHOW_CONTACT: show_contact,
    States.GET_USERNAME: get_user_question,
    States.USERNAME_AFTER_RETURNING: get_username_after_returning_back,
    States.SHOW_QUESTION: select_assistance,
}
