from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.constants.messages import ANSWER_TO_USER_MESSAGE
from bot.handlers.back_handler import back_button
from bot.keyboards.get_back import get_back_keyboard


async def answer_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Удаление и ответ на любое сообщение пользователя."""
    # Удаляем сообщение пользователя
    await update.message.delete()

    # Достаем последний ID сообщения бота
    user_message_id = update.message.message_id
    bot_last_message_id = user_message_id - 1

    # Если последний ID доступен, пробуем изменить сообщение
    if bot_last_message_id:
        try:
            await context.bot.edit_message_text(
                ANSWER_TO_USER_MESSAGE,
                chat_id=update.effective_chat.id,
                message_id=bot_last_message_id,
                reply_markup=get_back_keyboard(),
            )
        except Exception as e:
            # Если изменение не получилось, выдаем ошибку
            print(f"Failed to edit message: {e}")

    # Если сообщение от бота не найдено или его нет, пишем новое сообщение с текстом и инлайном
    if not bot_last_message_id:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ANSWER_TO_USER_MESSAGE,
            reply_markup=get_back_keyboard(),
        )

    # Обновляем последнее сообщение с ID = сообщению бота
    context.user_data["last_bot_message_id"] = bot_last_message_id

    await back_button(update, context)


# Определяем хендлер ответа на сообщения пользователя
answer_all_messages_handler = MessageHandler(filters.ALL, answer_all_messages)

# Определяем хендлер кнопки назад
back_button_handler = CallbackQueryHandler(back_button, pattern=r"^back$")
