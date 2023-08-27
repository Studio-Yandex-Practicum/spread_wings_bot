import logging

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
from config.settings import DEFAULT_RECEIVER
from core.mailing import send_email

CONTACT_NAME = "name"
CONTACT = "contact"
CONTACT_TYPE = "contact_type"
EMAIL = "EMAIL"
VALIDATION_EMAIL_ERROR_MESSAGE = "Допущена ошибка при вводе данных:\n\nАдрес электронной почты введен в некорректном формате.\n\nНеобходимый фомат: test@test.ru\n\nСкорректируйте email адрес и попробуйте ещё раз!"
VALIDATION_PHONE_ERROR_MESSAGE = "Допущена ошибка при вводе данных:\n\nНомер телефона введен в некорректном формате.\n\nНеобходимый фомат: +7ххххххххх \n\nСкорректируйте номер телефона и попробуйте ещё раз!"
PHONE = "PHONE"
QUESTION = "question"
QUESTION_TYPE = "question_type"
TELEGRAM = "TELEGRAM"
TELEGRAM_USERNAME_INDEX = "@"
SUBJECT_OF_RHE_ERROR_MESSAGE = "При обращении пользователя возникла ошибка!"


@debug_logger(
    state=States.GET_USER_QUESTION, run_functions_debag_loger="get_question"
)
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
    return States.GET_USERNAME


@debug_logger(
    state=States.GET_USERNAME,
    run_functions_debag_loger="get_username_after_returning_back",
)
async def get_username_after_returning_back(
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
    return States.GET_USERNAME


@debug_logger(
    state=States.SEND_EMAIL, run_functions_debag_loger="get_username"
)
async def get_username(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Name field handler."""
    name = update.message.text
    context.user_data[CONTACT_NAME] = name
    await update.message.reply_text(
        CONTACT_TYPE_MESSAGE.format(name=name.capitalize()),
        reply_markup=ask_question_keyboard_markup,
    )
    return States.SEND_EMAIL


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
    state=States.GET_CONTACT,
    run_functions_debag_loger="send_email_to_region_coordinator",
)
async def send_email_to_region_coordinator(
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
            return States.SEND_EMAIL
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
            logging.error(error, exc_info=True)
            await send_email(
                subject=SUBJECT_OF_RHE_ERROR_MESSAGE,
                message=f"У нас проблема: {error}",
                recipients=[
                    DEFAULT_RECEIVER,
                ],
            )
            await query.edit_message_text(
                QUESTION_FAIL,
                reply_markup=assistance_keyboard_markup,
            )
        return States.GET_ASSISTANCE
    await query.edit_message_text(text=ENTER_YOUR_CONTACT[contact_type])
    return States.GET_CONTACT


@debug_logger(
    state=States.GET_ASSISTANCE,
    run_functions_debag_loger="get_contact_and_send_email_to_region_coordinator",
)
async def get_contact_and_send_email_to_region_coordinator(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Contact field handler."""
    raw_contact = update.message.text
    try:
        if context.user_data[CONTACT_TYPE] == EMAIL:
            UserContacts(email=raw_contact)
    except ValidationError as error:
        logging.error(error)
        await update.message.reply_text(text=VALIDATION_EMAIL_ERROR_MESSAGE)
    try:
        if context.user_data[CONTACT_TYPE] == PHONE:
            UserContacts(phone=raw_contact)
    except ValidationError as error:
        logging.error(error)
        await update.message.reply_text(text=VALIDATION_PHONE_ERROR_MESSAGE)
        return States.GET_CONTACT
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
        logging.error(error, exc_info=True)
        await send_email(
            subject=SUBJECT_OF_RHE_ERROR_MESSAGE,
            message=f"У нас проблема: {error}",
            recipients=[
                DEFAULT_RECEIVER,
            ],
        )
        await update.message.reply_text(
            QUESTION_FAIL,
            reply_markup=assistance_keyboard_markup,
        )
    return States.GET_ASSISTANCE
