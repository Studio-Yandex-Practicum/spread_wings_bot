from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.back_functions import ASK_FUNCTIONS
from bot.constants.states.ask_question_states import AskQuestionStates


async def ask_back_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Возврат в предыдущее состояние в форме "Задайте Ваш вопрос"."""
    query = update.callback_query
    context.user_data.popitem()
    command = query.data.replace("ask_back_", "")
    if command == "cancel":
        context.user_data.clear()
        return AskQuestionStates.END
    await ASK_FUNCTIONS.get(command)(update, context)
    return command
