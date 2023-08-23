from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.handlers.service_handlers import FUNCTIONS


@debug_logger(state="Back to previous state", run_function_name="back_button")
async def back_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Возврат в предыдущее состояние."""
    query = update.callback_query
    command = query.data.replace("back_to_", "")
    return await FUNCTIONS.get(command)(update, context)
