from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import (
    ASSISTANCE_TYPE_MESSAGE,
    CONTACT_SHOW_MESSAGE,
    GET_USER_QUESTION,
    SELECT_FUND_PROGRAM,
    SELECT_QUESTION,
)
from bot.constants.patterns import FUND_PROGRAMS, HELP_TYPE
from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.assistance import (
    build_fund_program_keyboard,
    build_question_keyboard,
    build_region_keyboard,
    contact_type_keyboard_markup,
    to_the_original_state_and_previous_step_keyboard_markup,
)
from bot.keyboards.assistance_types import assistance_types_keyboard_markup
from bot.keyboards.utils.callback_data_parse import parse_callback_data
from bot_settings.models import BotSettings

DEFAULT_PAGE = 1


@debug_logger(state=States.REGION, run_functions_debug_loger="get_assistance")
async def get_assistance(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Select a region of assistance."""
    await update.callback_query.answer()
    keyboard = await build_region_keyboard()
    assistance_message = await BotSettings.objects.aget(
        key="assistance_message"
    )
    await update.callback_query.edit_message_text(
        text=assistance_message.value, reply_markup=keyboard
    )
    return States.REGION


@debug_logger(
    state=States.ASSISTANCE_TYPE,
    run_functions_debug_loger="select_type_of_assistance",
)
async def select_type_of_assistance(
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


@debug_logger(
    state=States.ASSISTANCE_TYPE,
    run_functions_debug_loger="select_assistance",
)
async def select_assistance(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Select assistance type."""
    query = update.callback_query
    question_type, page_number = parse_callback_data(query.data, HELP_TYPE)
    page_number = page_number or DEFAULT_PAGE
    if question_type:
        context.user_data[States.GET_USERNAME] = question_type
    context.user_data[States.QUESTION_TYPE] = question_type
    region = context.user_data.get(States.REGION)
    await query.answer()
    keyboard = await build_question_keyboard(
        region,
        context.user_data[States.GET_USERNAME],
        page_number,
    )
    if query.message.reply_markup.to_json() != keyboard.markup:
        await query.edit_message_text(
            text=SELECT_QUESTION,
            reply_markup=keyboard.markup,
        )


@debug_logger(
    state=States.FUND_PROGRAMS, run_functions_debug_loger="fund_programs"
)
async def fund_programs(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show fund programs."""
    query = update.callback_query
    region = context.user_data.get(States.REGION)
    _, page_number = parse_callback_data(query.data, FUND_PROGRAMS)
    page_number = page_number or DEFAULT_PAGE
    await query.answer()
    keyboard = await build_fund_program_keyboard(region, page_number)
    if query.message.reply_markup.to_json() != keyboard.markup:
        await query.edit_message_text(
            text=SELECT_FUND_PROGRAM,
            reply_markup=keyboard.markup,
        )


@debug_logger(
    state=States.GET_USER_QUESTION,
    run_functions_debug_loger="get_user_question",
)
async def get_user_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Ask question handler."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=GET_USER_QUESTION,
        reply_markup=to_the_original_state_and_previous_step_keyboard_markup,
    )
    return States.GET_USER_QUESTION


@debug_logger(
    state=States.CONTACT_US, run_functions_debug_loger="contact_with_us"
)
async def contact_with_us(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Ask question and show contacts."""
    query = update.callback_query
    context.user_data[States.QUESTION_TYPE] = "COMMON_QUESTION"
    await query.answer()
    await query.edit_message_text(
        text=CONTACT_SHOW_MESSAGE,
        reply_markup=contact_type_keyboard_markup,
    )
    return States.CONTACT_US
