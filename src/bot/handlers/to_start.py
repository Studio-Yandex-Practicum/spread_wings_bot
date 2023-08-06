from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.states.ask_question_states import AskQuestionStates


def check_for_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка в callback 'отмена', чтобы вернуть пользователя в начало."""
    if update.callback_query is not None:
        if update.callback_query.data == "cancel":
            return AskQuestionStates.END
