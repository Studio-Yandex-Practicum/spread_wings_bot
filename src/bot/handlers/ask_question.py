from pydantic import ValidationError
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.messages import (
    CONTACT_TYPE_MESSAGE,
    ENTER_YOUR_CONTCACT,
    QUESTION_FAIL,
    START_MESSAGE,
    THANKS_FOR_THE_QUESTION,
    WHAT_IS_YOUR_NAME_MESSAGE,
)
from bot.constants.states.ask_question_states import AskQuestionStates
from bot.constants.states.main_states import States
from bot.keyboards.ask_question import ask_question_keyboard_markup
from bot.keyboards.assistance import assistance_keyboard_markup
from bot.validators import Contacts
from mailing import BotMailer, MailForm


async def restart(update: Update):
    """Функция перезапуска бота при подаче команды '/start'."""
    await update.message.reply_text(
        START_MESSAGE, reply_markup=assistance_keyboard_markup
    )
    return States.ASSISTANCE


async def get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Question field handler."""
    question = update.message.text
    context.user_data["question"] = question
    if question == "/start":
        return await restart(update)
    await update.message.reply_text(WHAT_IS_YOUR_NAME_MESSAGE)
    return AskQuestionStates.QUESTION


async def get_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Name field handler."""
    name = update.message.text
    if name == "/start":
        return await restart(update)
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
    await query.answer()
    contact_type = query.data
    context.user_data["contact_type"] = contact_type
    if contact_type == "TELEGRAM":
        context.user_data["contact"] = "@" + query.message.chat.username
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
    if raw_contact == "/start":
        return await restart(update)
    try:
        if context.user_data["contact_type"] == "EMAIL":
            Contacts(email=raw_contact)
        else:
            Contacts(phone=raw_contact)
    except ValidationError:
        await update.message.reply_text(text="Неверный формат")
        return AskQuestionStates.ENTER_YOUR_CONTACT

    context.user_data["contact"] = raw_contact
    try:
        question_form = MailForm(
            name=context.user_data["name"],
            contact=context.user_data["contact"],
            question=context.user_data["question"],
        )
        await BotMailer.send_message(question_form)
        await update.message.reply_text(
            THANKS_FOR_THE_QUESTION, reply_markup=assistance_keyboard_markup
        )
    except Exception as error:
        await update.message.reply_text(
            QUESTION_FAIL.format(error),
            reply_markup=assistance_keyboard_markup,
        )
    return AskQuestionStates.END
