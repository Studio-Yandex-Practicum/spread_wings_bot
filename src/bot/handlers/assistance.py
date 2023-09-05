from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.patterns import FUND_PROGRAMS, GET_ASSISTANCE, HELP_TYPE
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


@debug_logger(
    state=States.GET_ASSISTANCE, run_functions_debug_loger="get_assistance"
)
async def get_assistance(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Select a region of assistance."""
    query = update.callback_query
    callback_data = query.data.replace("back_to_", "")
    _, page_number = parse_callback_data(callback_data, GET_ASSISTANCE)
    page_number = page_number or DEFAULT_PAGE
    await query.answer()
    keyboard = await build_region_keyboard(page_number)
    assistance_message = await BotSettings.objects.aget(
        key="assistance_message"
    )
    if query.message.reply_markup.to_json() != keyboard.markup:
        await query.edit_message_text(
            text=assistance_message.value,
            reply_markup=keyboard.markup,
        )
    return States.GET_ASSISTANCE


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
    select_type_of_assistance_message = await BotSettings.objects.aget(
        key="select_type_of_help"
    )
    await update.callback_query.edit_message_text(
        text=select_type_of_assistance_message.value,
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
    selected_type_assistance_message = await BotSettings.objects.aget(
        key="selected_type_assistance"
    )
    if query.message.reply_markup.to_json() != keyboard.markup:
        await query.edit_message_text(
            text=selected_type_assistance_message.value,
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
    fund_programs_message = await BotSettings.objects.aget(key="fund_programs")
    if query.message.reply_markup.to_json() != keyboard.markup:
        await query.edit_message_text(
            text=fund_programs_message.value,
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
    ask_question_message = await BotSettings.objects.aget(key="ask_question")
    await query.edit_message_text(
        text=ask_question_message.value,
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
    contact_with_us_message = await BotSettings.objects.aget(
        key="contact_with_us"
    )
    await query.edit_message_text(
        text=contact_with_us_message.value,
        reply_markup=contact_type_keyboard_markup,
    )
    return States.CONTACT_US
