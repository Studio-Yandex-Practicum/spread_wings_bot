from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import ASSISTANCE_TYPE_MESSAGE
from bot.constants.states import States
from bot.handlers.assistance import receive_assistance
from bot.keyboards.assistance_types import assistance_types_keyboard_markup


async def select_type_of_help(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> States:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=assistance_types_keyboard_markup
    )
    return States.ASSISTANCE_TYPE


async def legal_assistance(update: Update,
                           context: ContextTypes.DEFAULT_TYPE):
    pass


async def social_assistance(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    pass


async def psychological_assistance(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    pass


async def fund_programs(update: Update,
                       context: ContextTypes.DEFAULT_TYPE):
    pass


async def contact_us(update: Update,
                     context: ContextTypes.DEFAULT_TYPE):
    pass


async def back_to_region(update: Update,
                         context: ContextTypes.DEFAULT_TYPE):
    return await receive_assistance(update, context)
