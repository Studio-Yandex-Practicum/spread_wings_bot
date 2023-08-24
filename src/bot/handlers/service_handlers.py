from typing import Any, Awaitable, Callable

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.constants.messages import ANSWER_TO_USER_MESSAGE
from bot.constants.states import States
from bot.handlers.ask_question import ask_name
from bot.handlers.assistance import (
    ask_question,
    contact_with_us,
    fund_programs,
    receive_assistance,
    select_assistance,
    select_type_of_help,
    show_contact,
)
from bot.handlers.debug_handlers import debug_logger
from bot.handlers.main_handlers import start


@debug_logger(
    state=States.ANSWER_TO_USER_MESSAGE,
    run_functions_debag_loger="answer_all_messages",
)
async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает и отвечает на любое введенное пользователем сообщение."""
    await update.message.delete()
    await update.message.reply_text(ANSWER_TO_USER_MESSAGE)


answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)


FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.ASSISTANCE.value: start,
    States.ASSISTANCE_TYPE: select_type_of_help,
    States.CONTACT_US: contact_with_us,
    States.FUND_PROGRAMS: fund_programs,
    States.QUESTIONS_AND_CONTACTS: select_assistance,
    States.REGION: receive_assistance,
    States.SHOW_CONTACT: show_contact,
    States.QUESTION: ask_question,
    States.NAME: ask_name,
    States.SHOW_QUESTION: select_assistance,
}
