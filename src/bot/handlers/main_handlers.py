from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.constants import ASSISTANCE, HELP_MESSAGE, START_MESSAGE
from bot.keyboards.assistance import assistance_keyboard_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Точка старта бота. Приветствие. Две кнопки."""
    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=assistance_keyboard_markup
    )
    return ASSISTANCE


async def help_command(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Функция показывает информацию о том, как использовать этот бот"""
    await update.message.reply_text(HELP_MESSAGE)


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
