from telegram import MenuButtonCommands, Update
from telegram.ext import CommandHandler, ContextTypes

from bot.constants.commands import COMMANDS
from bot.constants.messages import MENU_MESSAGE


async def update_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Функция обновляет список команд и кнопку меню."""
    await context.bot.set_my_commands(commands=COMMANDS)
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    await update.message.reply_text(MENU_MESSAGE)


menu_handler = CommandHandler("upmenu", update_menu)
