from pydantic import ValidationError
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants.messages import (
    CONTACT_TYPE_MESSAGE,
    ENTER_YOUR_CONTCACT,
    THANKS_FOR_THE_QUESTION,
    WHAT_IS_YOUR_NAME_MESSAGE,
)
from bot.constants.patterns import CONTACT_TYPE_PATTERN
from bot.constants.states.ask_question_states import AskQuestionStates
from bot.constants.states.main_states import PATTERN, States
from bot.handlers.main_handlers import start_handler
from bot.keyboards.ask_question import ask_question_keyboard_markup
from bot.keyboards.assistance import assistance_keyboard_markup
from bot.validators import Contacts


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
    await query.answer()
    contact_type = query.data
    context.user_data["contact_type"] = contact_type
    if contact_type == "TELEGRAM":
        context.user_data["contact"] = "@" + query.message.chat.username
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
            Contacts(email=raw_contact)
        else:
            Contacts(phone=raw_contact)
    except ValidationError:
        await update.message.reply_text(text="Неверный формат")
        return AskQuestionStates.ENTER_YOUR_CONTACT

    context.user_data["contact"] = raw_contact
    await update.message.reply_text(
        THANKS_FOR_THE_QUESTION, reply_markup=assistance_keyboard_markup
    )
    return AskQuestionStates.END


ask_question_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^.*$"), get_question),
    ],
    states={
        AskQuestionStates.QUESTION: [
            MessageHandler(filters.Regex("^.*$"), get_name),
        ],
        AskQuestionStates.NAME: [
            CallbackQueryHandler(
                get_name,
                pattern=PATTERN.format(
                    state=AskQuestionStates.CONTACT_TYPE.value
                ),
            ),
        ],
        AskQuestionStates.CONTACT_TYPE: [
            CallbackQueryHandler(
                select_contact_type, pattern=CONTACT_TYPE_PATTERN
            )
        ],
        AskQuestionStates.ENTER_YOUR_CONTACT: [
            MessageHandler(filters.Regex("^.*$"), get_contact)
        ],
    },
    fallbacks=[start_handler],
    map_to_parent={
        AskQuestionStates.END: States.ASSISTANCE,
    },
)
