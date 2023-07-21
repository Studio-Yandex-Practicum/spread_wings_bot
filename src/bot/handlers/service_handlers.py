from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.constants.messages import ANSWER_TO_USER_MESSAGE


async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает и отвечает на любое введенное пользователем сообщение."""
    await update.message.delete()
    await update.message.reply_text(ANSWER_TO_USER_MESSAGE)


answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)
