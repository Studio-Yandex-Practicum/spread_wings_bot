from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.contacts import Contacts
from bot.constants.messages import ASSISTANCE_MESSAGE, ASSISTANCE_TYPE_MESSAGE
from bot.constants.regions import Regions
from bot.constants.states.main_states import States
from bot.keyboards.assistance import (
    assistance_questions_keyboard_contact,
    contact_show_keyboard_markup,
    region_keyboard_markup,
)
from bot.keyboards.assistance_types import (
    assistance_questions_keyboard_markup,
    assistance_types_keyboard_markup,
)


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
    await query.answer()
    await query.edit_message_text(
        text="Выбор вопроса из списка",
        reply_markup=assistance_questions_keyboard_markup,
    )
    return States.SELECTED_TYPE


async def fund_programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для вывода информации о программах Фонда."""
    pass


async def back_to_region(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Возврат в родительское меню (выбор региона)."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    )
    return States.REGION


async def contact_with_us(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Связаться с нами."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Выбор вопроса из списка",
        reply_markup=assistance_questions_keyboard_contact,
    )
    return States.SELECTED_TYPE


async def show_contact(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Показываем контакт регионального куратора."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=Contacts[context.user_data[States.REGION]].value,
        reply_markup=contact_show_keyboard_markup,
    )
    return States.ASSISTANCE_TYPE
