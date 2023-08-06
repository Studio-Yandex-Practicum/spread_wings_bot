from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    BACK_ASSISTANCE_BUTTON,
    BACK_BUTTON,
    EMAIL,
    PHONE,
    TELEGRAM,
)
from bot.constants.states.ask_question_states import AskQuestionStates
from bot.constants.states.main_states import States

ask_question_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"ask_back_{AskQuestionStates.END}",
        ),
        InlineKeyboardButton(
            text=BACK_ASSISTANCE_BUTTON,
            callback_data="cancel",
        ),
    ]
]

ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)

name_question_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASK_QUESTION.value}",
        ),
        InlineKeyboardButton(
            text=BACK_ASSISTANCE_BUTTON,
            callback_data="cancel",
        ),
    ]
]

name_question_keyboard_markup = InlineKeyboardMarkup(name_question_keyboard)

contact_type_question_keyboard = [
    [
        InlineKeyboardButton(text=EMAIL, callback_data="EMAIL"),
        InlineKeyboardButton(text=PHONE, callback_data="PHONE"),
        InlineKeyboardButton(text=TELEGRAM, callback_data="TELEGRAM"),
    ],
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"ask_back_{AskQuestionStates.QUESTION.value}",
        ),
        InlineKeyboardButton(
            text=BACK_ASSISTANCE_BUTTON,
            callback_data="cancel",
        ),
    ],
]

contact_type_question_keyboard_markup = InlineKeyboardMarkup(
    contact_type_question_keyboard
)
