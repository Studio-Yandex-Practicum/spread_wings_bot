from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.patterns import SHOW_CONTACT, SHOW_PROGRAM, SHOW_QUESTION
from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.assistance import (
    contact_show_keyboard_markup,
    question_show_keyboard_markup,
    show_fund_program_keyboard_markup,
)
from bot.keyboards.utils.callback_data_parse import parse_callback_data
from bot.models import Coordinator, FundProgram, Question
from core.utils import convert_br_tags_to_telegram_message

HTML_REPLY_TEXT = "<strong>{title}</strong>\n\n{text}"
EDIT_MESSAGE_PARSE_MODE = "HTML"
FUND_PROGRAM_DOES_NOT_EXIST_ERROR_MESSAGE = "Program does not exists!"
QUESTION_DOES_NOT_EXIST_ERROR_MESSAGE = "Question does not exists!"
REGION_C = "Региональный координатор:"
CHIEF_C = "Главный координатор:"


@debug_logger(state=SHOW_CONTACT, run_functions_debug_loger="show_contact")
async def show_contact(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Show contacts of the regional curator."""
    query = update.callback_query
    coordinator = await Coordinator.objects.filter(
        region__region_key=context.user_data["region"]
    ).afirst()
    chief = await Coordinator.objects.filter(is_chief=True).afirst()
    await query.answer()
    await query.edit_message_text(
        text=f"{CHIEF_C if chief and chief != coordinator else ''}\n"
        f"{chief.__repr__() if chief and chief != coordinator else ''}\n"
        f"\n{REGION_C if chief != coordinator else CHIEF_C}\n"
        f"{coordinator!r}",
        reply_markup=contact_show_keyboard_markup,
    )
    return States.SHOW_CONTACT


@debug_logger(
    state=States.SHOW_QUESTION, run_functions_debug_loger="show_question"
)
async def show_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Show information about the selected question."""
    query = update.callback_query
    _, question_id = parse_callback_data(query.data, SHOW_QUESTION)
    reply_text = QUESTION_DOES_NOT_EXIST_ERROR_MESSAGE
    if question_id:
        try:
            question = await Question.objects.aget(id=question_id)
            reply_text = convert_br_tags_to_telegram_message(
                HTML_REPLY_TEXT.format(
                    title=question.question, text=question.answer
                )
            )
        except Question.DoesNotExist:
            pass
    await query.answer()
    await query.edit_message_text(
        text=reply_text,
        parse_mode=EDIT_MESSAGE_PARSE_MODE,
        reply_markup=question_show_keyboard_markup,
    )


@debug_logger(
    state=States.SHOW_PROGRAM, run_functions_debug_loger="show_program"
)
async def show_program(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Show selected program data info."""
    query = update.callback_query
    _, program_id = parse_callback_data(query.data, SHOW_PROGRAM)
    reply_text = FUND_PROGRAM_DOES_NOT_EXIST_ERROR_MESSAGE
    if program_id:
        try:
            fund_program = await FundProgram.objects.aget(id=program_id)
            reply_text = convert_br_tags_to_telegram_message(
                HTML_REPLY_TEXT.format(
                    title=fund_program.title, text=fund_program.fund_text
                )
            )
        except FundProgram.DoesNotExist:
            pass
    await query.answer()
    await query.edit_message_text(
        text=reply_text,
        parse_mode=EDIT_MESSAGE_PARSE_MODE,
        reply_markup=show_fund_program_keyboard_markup,
    )
