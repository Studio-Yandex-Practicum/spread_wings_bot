import re

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants.ask_question_states import AskQuestionStates
from bot.constants.messages import (
    CONTACT_TYPE_MESSAGE,
    ENTER_YOUR_CONTCACT,
    THANKS_FOR_THE_QUESTION,
    WHAT_IS_YOUR_NAME_MESSAGE,
)
from bot.constants.states import PATTERN, States
from bot.constants.validate_patterns import ContactValidate
from bot.handlers.main_handlers import start_handler
from bot.keyboards.ask_question import ask_question_keyboard_markup
from bot.keyboards.assistance import assistance_keyboard_markup


async def get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Обработчик вопроса."""
    question = update.message.text
    context.user_data["question"] = question
    await update.message.reply_text(WHAT_IS_YOUR_NAME_MESSAGE)
    return AskQuestionStates.QUESTION


async def get_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Обработчик имени вопрошающего."""
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
    """Обработчик типа связи."""
    query = update.callback_query
    await query.answer()
    contact_type = query.data.split("_")[1]
    context.user_data["contact_type"] = contact_type
    if contact_type == "TELEGRAM":
        context.user_data["contact"] = "@" + query.message.chat.username
        return AskQuestionStates.THANKS_FOR_THE_QUESTION
    await query.edit_message_text(text=ENTER_YOUR_CONTCACT[contact_type])
    return AskQuestionStates.ENTER_YOUR_CONTACT


async def get_contact(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AskQuestionStates:
    """Обработчик контакта."""
    contact = update.message.text
    if re.match(
        getattr(ContactValidate, context.user_data["contact_type"]), contact
    ):
        context.user_data["contact"] = contact
        await update.message.reply_text(
            THANKS_FOR_THE_QUESTION, reply_markup=assistance_keyboard_markup
        )
        return AskQuestionStates.END
    await update.message.reply_text(text="Неверный формат")
    return AskQuestionStates.ENTER_YOUR_CONTACT


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
                select_contact_type, pattern="^contact_(EMAIL|PHONE|TELEGRAM)$"
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
