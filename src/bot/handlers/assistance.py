from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.contacts import Contacts
from bot.constants.messages import (
    ASK_YOUR_QUESTION,
    ASSISTANCE_MESSAGE,
    ASSISTANCE_TYPE_MESSAGE,
    CONTACT_SHOW_MESSAGE,
    SELECT_QUESTION,
)
from bot.constants.states.main_states import States
from bot.constants.types_of_assistance import AssistanceTypes
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.assistance import (
    build_region_keyboard,
    contact_show_keyboard_markup,
    contact_type_keyboard_markup,
    to_the_original_state_and_previous_step_keyboard_markup,
)
from bot.keyboards.assistance_types import (
    assistance_questions_keyboard_markup,
    assistance_types_keyboard_markup,
)


@debug_logger(name="receive_assistance")
async def receive_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для выбора региона оказания помощи."""
    await update.callback_query.answer()
    keyboard = await build_region_keyboard()
    await update.callback_query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=keyboard
    )
    return States.REGION


@debug_logger(name="select_type_of_help")
async def select_type_of_help(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Выбор типа необходимой для оказания помощи."""
    context.user_data[States.REGION] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=assistance_types_keyboard_markup,
    )
    return States.ASSISTANCE_TYPE


@debug_logger(name="selected_type_assistance")
async def select_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для выбранного типа помощи."""
    query = update.callback_query
    question_type = query.data
    context.user_data["question_type"] = AssistanceTypes[question_type].value
    await query.answer()
    await query.edit_message_text(
        text=SELECT_QUESTION,
        reply_markup=assistance_questions_keyboard_markup,
    )
    return States.QUESTIONS_AND_CONTACTS


@debug_logger(name="fund_programs")
async def fund_programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для вывода информации о программах Фонда."""
    pass


@debug_logger(name="ask_question")
async def ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для задания вопроcа."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASK_YOUR_QUESTION,
        reply_markup=to_the_original_state_and_previous_step_keyboard_markup,
    )
    return States.ASK_QUESTION


@debug_logger(name="contact_with_us")
async def contact_with_us(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Ask question and Show contacts."""
    query = update.callback_query
    context.user_data["question_type"] = AssistanceTypes.COMMON_QUESTION.value
    await query.answer()
    await query.edit_message_text(
        text=CONTACT_SHOW_MESSAGE,
        reply_markup=contact_type_keyboard_markup,
    )
    return States.CONTACT_US


@debug_logger(name="show_contact")
async def show_contact(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Show contacts of the regional curator."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=Contacts[context.user_data[States.REGION]].value,
        reply_markup=contact_show_keyboard_markup,
    )
    return States.SHOW_CONTACT
