from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.constants import ASSISTANCE, START_MESSAGE
from bot.keyboards.assistance import assistance


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Написал для тестирования
    await update.message.reply_text(
        text=START_MESSAGE,
        reply_markup=assistance
    )
    return ASSISTANCE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
