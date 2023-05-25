from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.keyboards.main_keyboards import Kboards
from bot.constants import CHOOSE_REGION


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def choosing_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_keyboard = Kboards.choosing_region_keybord()
    await update.message.reply_text(CHOOSE_REGION, reply_markup=inline_keyboard)


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
choosing_region_handler = CommandHandler('choose_region', choosing_region)
