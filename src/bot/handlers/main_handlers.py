from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
