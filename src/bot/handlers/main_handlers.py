from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler

from bot.constants import HELP_MESSAGE, START_MESSAGE

ONE, TWO, THREE, FOUR = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Точка старта бота. Приветствие. Две кнопки."""
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(START_MESSAGE, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция показывает информацию о том, как использовать этот бот"""
    await update.message.reply_text(HELP_MESSAGE)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
