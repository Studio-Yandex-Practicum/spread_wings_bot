from typing import Any, Awaitable, Callable

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.constants.messages import ANSWER_TO_USER_MESSAGE
from bot.constants.states import States
from bot.handlers.ask_question import get_username_after_returning_back
from bot.handlers.assistance import (
    contact_us,
    fund_programs,
    get_assistance,
    get_user_question,
    select_type_of_assistance,
    show_contact,
)
from bot.handlers.debug_handlers import debug_logger
from bot.handlers.main_handlers import start


@debug_logger(name="answer_all_messages")
async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает и отвечает на любое введенное пользователем сообщение."""
    await update.message.delete()
    await update.message.reply_text(ANSWER_TO_USER_MESSAGE)


answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)


FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.ASSISTANCE_TYPE: select_type_of_assistance,
    States.CONTACT_US: contact_us,
    States.FUND_PROGRAMS: fund_programs,
    States.GET_ASSISTANCE.value: start,
    States.GET_USER_QUESTION: get_user_question,
    States.GET_USERNAME: get_username_after_returning_back,
    States.REGION: get_assistance,
    States.SHOW_CONTACT: show_contact,
}
