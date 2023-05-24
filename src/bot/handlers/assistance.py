from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler

from bot.handlers.main_handlers import start_handler
from bot.keyboards.assistance import assistance, donation, region
from bot.constants import (ASSISTANCE,
                           BACK,
                           DONATION_MESSAGE,
                           DONATION,
                           ASSISTANCE_MESSAGE,
                           REGION,
                           START_MESSAGE)


async def receive_assistance(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=region
    )
    return REGION


async def make_donation(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=DONATION_MESSAGE, reply_markup=donation)


async def back_to_start(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=START_MESSAGE, reply_markup=assistance
    )
    return ASSISTANCE


# TODO Полагаю надо создать отдельный файл, который
#  будет разрозненные по  хендлерам ConversationHandler'ы
#  собирать в один, либо не писать разрозненные ConversationHandler'ы,
#  а в отдельном файле написать один разветвленный
assistance_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            ASSISTANCE: [
                CallbackQueryHandler(receive_assistance, pattern=f'^{ASSISTANCE}$'),
                CallbackQueryHandler(make_donation, pattern=f'^{DONATION}$')
            ]
        },
        # TODO в дальнейшем думаю надо добавить stop_handler для fallbacks
        fallbacks=[
            CallbackQueryHandler(back_to_start, pattern=f'^{BACK}$'),
            start_handler,
        ],
    )
