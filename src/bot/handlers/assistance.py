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
from bot.constants.regions import Regions
from bot.constants.states.main_states import States
from bot.keyboards.ask_question import ask_question_keyboard_markup
from bot.keyboards.assistance import (
    contact_show_keyboard_markup,
    contact_type_keyboard_markup,
    region_keyboard_markup,
)
from bot.keyboards.assistance_types import (
    assistance_questions_keyboard_markup,
    assistance_types_keyboard_markup,
)


async def receive_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для выбора региона оказания помощи."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    )
    return States.REGION


async def select_type_of_help(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Выбор типа необходимой для оказания помощи."""
    query = update.callback_query
    if query.data in [reg.name for reg in Regions]:
        context.user_data[States.REGION] = query.data
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=assistance_types_keyboard_markup,
    )
    return States.ASSISTANCE_TYPE


async def selected_type_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик для выбранного типа помощи."""
    query = update.callback_query
    question_type = query.data
    context.user_data["question_type"] = question_type
    await query.answer()
    await query.edit_message_text(
        text=SELECT_QUESTION,
        reply_markup=assistance_questions_keyboard_markup,
    )
    return States.QUESTIONS_AND_CONTACTS


async def fund_programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для вывода информации о программах Фонда."""
    pass


async def ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для задания вопроcа."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASK_YOUR_QUESTION, reply_markup=ask_question_keyboard_markup
    )
    return States.ASK_QUESTION


async def contact_with_us(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Ask question and Show contacts."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=CONTACT_SHOW_MESSAGE,
        reply_markup=contact_type_keyboard_markup,
    )
    return States.CONTACT_US


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
