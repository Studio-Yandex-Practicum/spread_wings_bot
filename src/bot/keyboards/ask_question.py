from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    BACK_BUTTON,
    BACK_START_BUTTON,
    EMAIL,
    PHONE,
    TELEGRAM
)
from bot.constants.states.main_states import States
from bot.constants.states.ask_question_states import AskQuestionStates


question_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}"
        ),
        InlineKeyboardButton(
            text=BACK_START_BUTTON,
            callback_data=f"back_to_{AskQuestionStates.CANCEL.value}"
        )
    ]
]

question_keyboard_markup = InlineKeyboardMarkup(question_keyboard)

name_question_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASK_QUESTION}"
        ),
        InlineKeyboardButton(
            text=BACK_START_BUTTON,
            callback_data=f"cancel"
        )
    ]
]

name_question_keyboard_markup = InlineKeyboardMarkup(name_question_keyboard)

ask_question_keyboard = [
    [
        InlineKeyboardButton(text=EMAIL, callback_data="EMAIL"),
        InlineKeyboardButton(text=PHONE, callback_data="PHONE"),
        InlineKeyboardButton(text=TELEGRAM, callback_data="TELEGRAM"),
    ],
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"ask_back_{AskQuestionStates.QUESTION.value}"
        ),
        InlineKeyboardButton(
            text=BACK_START_BUTTON,
            callback_data=f"cancel"  # back_to_{States.ASSISTANCE_TYPE.value}
        )
    ]
]

ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)
