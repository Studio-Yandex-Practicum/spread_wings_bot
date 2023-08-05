import asyncio

from telegram import MenuButtonCommands, Update
from telegram.ext import CommandHandler, ContextTypes

from bot.constants.commands import COMMANDS
from bot.handlers.debug_handlers import debug_logger
from bot.constants.messages import HELP_MESSAGE, START_MESSAGE
from bot.constants.states.main_states import States
from bot.keyboards.assistance import build_assistance_keyboard


@debug_logger(name='start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """Точка старта бота. Приветствие. Две кнопки."""
    bot_commands, assistance_keyboard_markup = await asyncio.gather(
        context.bot.get_my_commands(), build_assistance_keyboard()
    )
    if not bot_commands:
        await context.bot.set_my_commands(commands=COMMANDS)
        await context.bot.set_chat_menu_button(
            menu_button=MenuButtonCommands()
        )
    if update.message is not None:
        await update.message.reply_text(
            START_MESSAGE, reply_markup=assistance_keyboard_markup
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            START_MESSAGE, reply_markup=assistance_keyboard_markup
        )
    return States.ASSISTANCE


@debug_logger(name='help_command')
async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Функция показывает информацию о том, как использовать этот бот."""
    await update.message.reply_text(HELP_MESSAGE)


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)
