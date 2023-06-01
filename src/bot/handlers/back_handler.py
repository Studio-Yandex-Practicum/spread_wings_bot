from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.back_functions import FUNCTIONS
from bot.constants.states import States


async def back_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Возврат в предыдущее состояние."""
    query = update.callback_query
    command = query.data[8:]
    await FUNCTIONS.get(command)(update, context)
    return command
