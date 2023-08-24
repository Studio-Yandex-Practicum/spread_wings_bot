from asgiref.sync import sync_to_async
from pydantic import ValidationError
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import (
    CONTACT_TYPE_MESSAGE,
    ENTER_YOUR_CONTACT,
    MESSAGE_FROM_TELEGRAM_BOT,
    NO_TELEGRAM_USERNAME,
    QUESTION_FAIL,
    THANKS_FOR_THE_QUESTION,
    WHAT_IS_YOUR_NAME_MESSAGE,
)
from bot.constants.states import States
from bot.handlers.debug_handlers import debug_logger
from bot.keyboards.ask_question import (
    ask_question_keyboard_markup,
    back_to_previous_step_keyboard_markup,
)
from bot.keyboards.assistance import build_assistance_keyboard
from bot.models import Coordinator
from bot.models_pydantic.users_questions import UserContacts, UserQuestion
from core.mailing import send_email

CONTACT_NAME = "name"
CONTACT = "contact"
CONTACT_TYPE = "contact_type"
EMAIL = "EMAIL"
VALIDATION_ERROR_MESSAGE = (
    "Допущена ошибка при вводе данных!\n\n{error}\n\nПопробуйте ещё раз!"
)
PHONE = "PHONE"
QUESTION = "question"
QUESTION_TYPE = "question_type"
TELEGRAM = "TELEGRAM"
TELEGRAM_USERNAME_INDEX = "@"


@debug_logger(state=States.QUESTION, run_functions_debag_loger="get_question")
async def get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Question field handler."""
    question = update.message.text
    context.user_data[QUESTION] = question
    await update.message.reply_text(
        WHAT_IS_YOUR_NAME_MESSAGE,
        reply_markup=back_to_previous_step_keyboard_markup,
    )
    return States.QUESTION


@debug_logger(state=States.NAME, run_functions_debag_loger="ask_name")
async def ask_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> States:
    """Ask name handler."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=WHAT_IS_YOUR_NAME_MESSAGE,
        reply_markup=back_to_previous_step_keyboard_markup,
    )
    return States.NAME


@debug_logger(state=States.CONTACT_TYPE, run_functions_debag_loger="get_name")
async def get_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Name field handler."""
    name = update.message.text
    context.user_data[CONTACT_NAME] = name
    await update.message.reply_text(
        CONTACT_TYPE_MESSAGE.format(name=name.capitalize()),
        reply_markup=ask_question_keyboard_markup,
    )
    return States.CONTACT_TYPE


@sync_to_async
def get_coordinator_email(context: ContextTypes.DEFAULT_TYPE):
    """Get coordinator email address."""
    coordinator = Coordinator.objects.get(
        region__region_key=context.user_data[States.REGION],
    )
    return coordinator.email_address


async def send_message_to_coordinator_email(
    context: ContextTypes.DEFAULT_TYPE, coordinator_email: str
) -> None:
    """Send email with question to coordinator email address."""
    question_form = UserQuestion(
        name=context.user_data[CONTACT_NAME],
        contact=context.user_data[CONTACT],
        question=context.user_data[QUESTION],
        question_type=context.user_data[QUESTION_TYPE],
    )
    await send_email(
        subject=MESSAGE_FROM_TELEGRAM_BOT,
        message=question_form.to_representation(),
        recipients=[
            coordinator_email,
        ],
    )


@debug_logger(
    state=States.ENTER_YOUR_CONTACT,
    run_functions_debag_loger="select_contact_type",
)
async def select_contact_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Type of contact field handler."""
    query = update.callback_query
    contact_type = context.user_data[CONTACT_TYPE] = query.data
    assistance_keyboard_markup = await build_assistance_keyboard()
    coordinator_email = await get_coordinator_email(context)
    if contact_type == TELEGRAM:
        if not query.message.chat.username:
            await context.bot.answer_callback_query(
                callback_query_id=update.callback_query.id,
                text=NO_TELEGRAM_USERNAME,
                show_alert=True,
            )
            return States.CONTACT_TYPE
        context.user_data[CONTACT] = "".join(
            [TELEGRAM_USERNAME_INDEX, query.message.chat.username]
        )
        try:
            await send_message_to_coordinator_email(
                context=context, coordinator_email=coordinator_email
            )
            await query.edit_message_text(
                THANKS_FOR_THE_QUESTION,
                reply_markup=assistance_keyboard_markup,
            ),
        except Exception as error:
            await query.edit_message_text(
                QUESTION_FAIL.format(error),
                reply_markup=assistance_keyboard_markup,
            )
        return States.ASSISTANCE
    await query.edit_message_text(text=ENTER_YOUR_CONTACT[contact_type])
    return States.ENTER_YOUR_CONTACT


@debug_logger(state=States.ASSISTANCE, run_functions_debag_loger="get_contact")
async def get_contact(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Contact field handler."""
    raw_contact = update.message.text
    try:
        if context.user_data[CONTACT_TYPE] == EMAIL:
            UserContacts(email=raw_contact)
        if context.user_data[CONTACT_TYPE] == PHONE:
            UserContacts(phone=raw_contact)
    except ValidationError as error:
        await update.message.reply_text(
            text=VALIDATION_ERROR_MESSAGE.format(error=error)
        )
        return States.ENTER_YOUR_CONTACT
    context.user_data[CONTACT] = raw_contact
    assistance_keyboard_markup = await build_assistance_keyboard()
    coordinator_email = await get_coordinator_email(context)
    try:
        await send_message_to_coordinator_email(
            context=context, coordinator_email=coordinator_email
        )
        await update.message.reply_text(
            THANKS_FOR_THE_QUESTION,
            reply_markup=assistance_keyboard_markup,
        )
    except Exception as error:
        await update.message.reply_text(
            QUESTION_FAIL.format(error),
            reply_markup=assistance_keyboard_markup,
        )
    return States.ASSISTANCE
