from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.back_functions import ASK_FUNCTIONS, FUNCTIONS
from bot.constants.states.ask_question_states import AskQuestionStates
from bot.constants.states.main_states import States


async def back_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Возврат в предыдущее состояние."""
    print('back_handler START')
    query = update.callback_query
    command = query.data.replace("back_to_", "")
    await FUNCTIONS.get(command)(update, context)
    print('back_handler OK')
    return command


async def ask_back_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    print('ask_back_handler START')
    query = update.callback_query
    command = query.data.replace("ask_back_", "")
    await ASK_FUNCTIONS.get(command)(update, context)
    print('ask_back_handler OK')
    return command
