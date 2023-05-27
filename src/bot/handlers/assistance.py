# Файл заглушка нужно будет обновить. Не добавлял клавиатуры

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import DONATION_MESSAGE, CHOOSE_REGION_MESSAGE
from bot.constants.states import States
from bot.keyboards.assistance import choose_region_keyboard_markup


async def make_donation(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=DONATION_MESSAGE)
    return States.DONATION


async def choose_region(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):
    """Выбор региона."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=CHOOSE_REGION_MESSAGE,
        reply_markup=choose_region_keyboard_markup
    )
    return States.REGION