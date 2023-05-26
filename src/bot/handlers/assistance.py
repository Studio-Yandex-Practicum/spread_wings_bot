from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.assistance import (assistance_keyboard_markup,
                                      donation_keyboard_markup,
                                      region_keyboard_markup)
from bot.constants.messages import (ASSISTANCE_MESSAGE,
                                    DONATION_MESSAGE,
                                    START_MESSAGE)
from bot.constants.states import States


async def receive_assistance(update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> States:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    )
    return States.REGION


async def make_donation(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=DONATION_MESSAGE, reply_markup=donation_keyboard_markup
    )


async def back_to_start(update: Update,
                        context: ContextTypes.DEFAULT_TYPE) -> States:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=START_MESSAGE, reply_markup=assistance_keyboard_markup
    )
    return States.ASSISTANCE
