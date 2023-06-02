from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import ASSISTANCE_MESSAGE
from bot.constants.states import States
from bot.keyboards.assistance import region_keyboard_markup


async def receive_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для выбор региона оказания помощи."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    )
    print(44444)
    return States.REGION


async def contact_us_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик Задать вопрос."""
    # await update.message.reply_text(
    #     'Великолепно! А теперь пришли мне свое'
    #     ' местоположение, или /skip если параноик..'
    # )
    await update.message.reply_text("ПРИВЕТ!")
    # query = update.callback_query
    # await query.answer()
    # await query.edit_message_text(
    #     text=ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    # )
    return States.CONTACT_US
