from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import BACK_BUTTON, EMAIL, PHONE, TELEGRAM
from bot.constants.states import States

ask_question_keyboard = [
    [
        InlineKeyboardButton(text=EMAIL, callback_data="EMAIL"),
        InlineKeyboardButton(text=PHONE, callback_data="PHONE"),
        InlineKeyboardButton(text=TELEGRAM, callback_data="TELEGRAM"),
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.USERNAME_AFTER_RETURNING.value}",
        ),
    ]
]

ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)

back_to_previous_step_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.GET_USERNAME.value}",
        )
    ],
]

back_to_previous_step_keyboard_markup = InlineKeyboardMarkup(
    back_to_previous_step_keyboard
)
