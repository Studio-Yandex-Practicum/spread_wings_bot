from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import (
    ASK_YOUR_QUESTION,
    ASSISTANCE_MESSAGE,
    ASSISTANCE_TYPE_MESSAGE,
    CONTACT_SHOW_MESSAGE,
    SELECT_QUESTION,
    Contacts,
)
from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.assistance import (
    build_question_keyboard,
    build_region_keyboard,
    contact_show_keyboard_markup,
    contact_type_keyboard_markup,
    parse_callback_data,
    to_the_original_state_and_previous_step_keyboard_markup,
)
from bot.keyboards.assistance_types import assistance_types_keyboard_markup
from bot.models import HelpTypes

DEFAULT_PAGE = 1
QUESTION_TYPE = "question_type"


@debug_logger(name="receive_assistance")
async def receive_assistance(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Select a region of assistance."""
    await update.callback_query.answer()
    keyboard = await build_region_keyboard()
    await update.callback_query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=keyboard
    )
    return States.REGION


@debug_logger(name="select_type_of_help")
async def select_type_of_help(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Select assistance type."""
    if States.ASSISTANCE_TYPE.value not in update.callback_query.data:
        context.user_data[States.REGION] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=assistance_types_keyboard_markup,
    )
    return States.ASSISTANCE_TYPE


@debug_logger(name="selected_type_assistance")
async def select_assistance(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Select assistance type."""
    query = update.callback_query
    question_type, page_number = parse_callback_data(query.data)

    if question_type:
        context.user_data[QUESTION_TYPE] = question_type

    page_number = page_number or DEFAULT_PAGE
    region = context.user_data.get(States.REGION)

    await query.answer()

    keyboard = await build_question_keyboard(
        region,
        context.user_data[QUESTION_TYPE],
        page_number,
    )
    if query.message.reply_markup.to_json() != keyboard.markup:
        await query.edit_message_text(
            text=SELECT_QUESTION,
            reply_markup=keyboard.markup,
        )


@debug_logger(name="fund_programs")
async def fund_programs(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show fund programs."""
    pass


@debug_logger(name="ask_question")
async def ask_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Ask question handler."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASK_YOUR_QUESTION,
        reply_markup=to_the_original_state_and_previous_step_keyboard_markup,
    )
    return States.ASK_QUESTION


@debug_logger(name="contact_with_us")
async def contact_with_us(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Ask question and show contacts."""
    query = update.callback_query
    context.user_data[QUESTION_TYPE] = HelpTypes.COMMON_QUESTION.value
    await query.answer()
    await query.edit_message_text(
        text=CONTACT_SHOW_MESSAGE,
        reply_markup=contact_type_keyboard_markup,
    )
    return States.CONTACT_US


@debug_logger(name="show_contact")
async def show_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Show contacts of the regional curator."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=Contacts[context.user_data[States.REGION]].value,
        reply_markup=contact_show_keyboard_markup,
    )
    return States.SHOW_CONTACT
