from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.patterns import SHOW_QUESTION
from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.assistance import question_show_keyboard_markup
from bot.keyboards.utils.callback_data_parse import parse_callback_data
from bot.models import Question


@debug_logger(
    state=States.SHOW_QUESTION, run_functions_debag_loger="show_question"
)
async def show_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Show information about the selected question."""
    query = update.callback_query
    _, question_id = parse_callback_data(query.data, SHOW_QUESTION)
    reply_text = "Question does not exists!"
    if question_id:
        try:
            question = await Question.objects.aget(id=question_id)
            reply_text = (
                f"Вопрос: {question.question} \nОтвет: {question.answer}"
            )
        except Question.DoesNotExist:
            pass
    await query.answer()
    await query.edit_message_text(
        text=reply_text, reply_markup=question_show_keyboard_markup
    )
