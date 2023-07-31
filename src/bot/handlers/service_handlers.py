import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.constants.messages import ANSWER_TO_USER_MESSAGE
from bot.keyboards.get_back import get_back_keyboard

logger = logging.getLogger("bot")


async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Удаление и ответ на любое сообщение пользователя."""
    await update.message.delete()

    user_message_id = update.message.message_id
    print(user_message_id)
    bot_last_message_id = user_message_id - 1
    print(bot_last_message_id)

    if bot_last_message_id:
        try:
            previous_state = context.user_data.get("previous_state")

            await context.bot.edit_message_text(
                ANSWER_TO_USER_MESSAGE,
                chat_id=update.effective_chat.id,
                message_id=bot_last_message_id,
                reply_markup=get_back_keyboard(previous_state),
            )
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")

    context.user_data["last_bot_message_id"] = bot_last_message_id


answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)
