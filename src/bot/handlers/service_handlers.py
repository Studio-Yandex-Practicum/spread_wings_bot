from telegram import MenuButtonCommands, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot.constants.commands import COMMANDS
from bot.constants.messages import ANSWER_TO_USER_MESSAGE, MENU_MESSAGE


async def update_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Функция обновляет список команд и кнопку меню."""
    await context.bot.set_my_commands(commands=COMMANDS)
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    await update.message.reply_text(MENU_MESSAGE)


async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает и отвечает на любое введенное пользователем сообщение."""
    await update.message.delete()
    await update.message.reply_text(ANSWER_TO_USER_MESSAGE)


menu_handler = CommandHandler("upmenu", update_menu)
answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)
