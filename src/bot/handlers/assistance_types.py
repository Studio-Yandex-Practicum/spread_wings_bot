from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import ASSISTANCE_TYPE_MESSAGE
from bot.constants.states.main_states import States
from bot.keyboards.assistance_types import (
    assistance_questions_keyboard_markup,
    assistance_types_keyboard_markup,
)


async def select_type_of_help(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Выбор типа необходимой для оказания помощи."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=assistance_types_keyboard_markup,
    )
    return States.ASSISTANCE_TYPE


async def selected_type_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик для выбранного типа помощи."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Выбор вопроса из списка",
        reply_markup=assistance_questions_keyboard_markup,
    )
    return States.SELECTED_TYPE


async def fund_programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для вывода информации о программах Фонда."""
    pass
