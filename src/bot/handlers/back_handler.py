from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.back_functions import FUNCTIONS, States
from bot.handlers.debug_handlers import debug_logger


@debug_logger(name='back_button')
async def back_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Возврат в предыдущее состояние."""
    query = update.callback_query
    return await FUNCTIONS.get(
        query.data.replace("back_to_", "")
    )(update, context)
