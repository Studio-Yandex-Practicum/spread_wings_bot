import asyncio

from telegram import MenuButtonCommands, Update
from telegram.ext import CommandHandler, ContextTypes

from bot.constants.buttons import COMMANDS
from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.assistance import build_assistance_keyboard
from bot_settings.models import BotSettings


@debug_logger(state=States.START, run_functions_debag_loger="start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """Bot start."""
    bot_commands, assistance_keyboard_markup = await asyncio.gather(
        context.bot.get_my_commands(), build_assistance_keyboard()
    )
    start_message = await BotSettings.objects.aget(key="start_message")
    if not bot_commands:
        await context.bot.set_my_commands(commands=COMMANDS)
        await context.bot.set_chat_menu_button(
            menu_button=MenuButtonCommands()
        )
    if update.message is not None:
        await update.message.reply_text(
            start_message.value, reply_markup=assistance_keyboard_markup
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            start_message.value, reply_markup=assistance_keyboard_markup
        )
    return States.GET_ASSISTANCE


@debug_logger(state=States.HELP, run_functions_debag_loger="help_command")
async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Show information on how to use this bot."""
    help_message = await BotSettings.objects.aget(key="help_message")
    await update.message.reply_text(help_message.value)


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)
