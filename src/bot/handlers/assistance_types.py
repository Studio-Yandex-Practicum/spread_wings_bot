from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import ASSISTANCE_MESSAGE, ASSISTANCE_TYPE_MESSAGE
from bot.constants.states import States
from bot.keyboards.assistance import region_keyboard_markup
from bot.keyboards.assistance_types import assistance_types_keyboard_markup


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


async def legal_assistance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для оказания юридической помощи."""
    pass


async def social_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик для оказания социальной помощи."""
    pass


async def psychological_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик для оказания психологической помощи."""
    pass


async def fund_programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для вывода информации о программах Фонда."""
    pass


async def back_to_region(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Возврат в родительское меню (выбор региона)."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    )
    return States.REGION
