import asyncio

from pydantic import ValidationError
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import (
    CONTACT_TYPE_MESSAGE,
    ENTER_YOUR_CONTCACT,
    NO_TELEGRAM_USERNAME,
    QUESTION_FAIL,
    THANKS_FOR_THE_QUESTION,
    WHAT_IS_YOUR_NAME_MESSAGE,
)
from bot.constants.states.ask_question_states import AskQuestionStates
from bot.keyboards.ask_question import ask_question_keyboard_markup
from bot.keyboards.assistance import assistance_keyboard_markup
from bot.models_pydantic.users_questions import UserContacts, UserQuestion
from core.mailing import send_email


async def get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Question field handler."""
    question = update.message.text
    context.user_data["question"] = question
    await update.message.reply_text(WHAT_IS_YOUR_NAME_MESSAGE)
    return AskQuestionStates.QUESTION


async def get_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Name field handler."""
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text(
        CONTACT_TYPE_MESSAGE.format(name=name.capitalize()),
        reply_markup=ask_question_keyboard_markup,
    )
    return AskQuestionStates.CONTACT_TYPE


async def select_contact_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Type of contact field handler."""
    query = update.callback_query
    contact_type = query.data
    context.user_data["contact_type"] = contact_type
    if contact_type == "TELEGRAM":
        if not query.message.chat.username:
            await context.bot.answer_callback_query(
                callback_query_id=update.callback_query.id,
                text=NO_TELEGRAM_USERNAME,
                show_alert=True,
            )
            return AskQuestionStates.CONTACT_TYPE
        context.user_data["contact"] = "@" + query.message.chat.username
        await query.answer()
        await query.edit_message_text(
            THANKS_FOR_THE_QUESTION, reply_markup=assistance_keyboard_markup
        )
        return AskQuestionStates.END
    await query.edit_message_text(text=ENTER_YOUR_CONTCACT[contact_type])
    return AskQuestionStates.ENTER_YOUR_CONTACT


async def get_contact(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Contact field handler."""
    raw_contact = update.message.text
    try:
        if context.user_data["contact_type"] == "EMAIL":
            UserContacts(email=raw_contact)
        else:
            UserContacts(phone=raw_contact)
    except ValidationError:
        await update.message.reply_text(text="Неверный формат")
        return AskQuestionStates.ENTER_YOUR_CONTACT

    context.user_data["contact"] = raw_contact
    try:
        question_form = UserQuestion(
            name=context.user_data["name"],
            contact=context.user_data["contact"],
            question=context.user_data["question"],
            question_type=context.user_data["question_type"],
        )
        await asyncio.gather(
            *[
                send_email(
                    subject="Вопрос из телеграм бота",
                    message=question_form.to_representation(),
                ),
                update.message.reply_text(
                    THANKS_FOR_THE_QUESTION,
                    reply_markup=assistance_keyboard_markup,
                ),
            ]
        )
    except Exception as error:
        await update.message.reply_text(
            QUESTION_FAIL.format(error),
            reply_markup=assistance_keyboard_markup,
        )
    return AskQuestionStates.END
