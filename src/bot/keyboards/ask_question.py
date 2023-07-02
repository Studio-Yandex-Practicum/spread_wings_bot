from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import EMAIL, PHONE, TELEGRAM, BACK_BUTTON
from bot.constants.states.main_states import States


ask_question_keyboard = [
    [
        InlineKeyboardButton(text=EMAIL, callback_data="EMAIL"),
        InlineKeyboardButton(text=PHONE, callback_data="PHONE"),
        InlineKeyboardButton(text=TELEGRAM, callback_data="TELEGRAM"),
    ]
]

back_to_keyboard = [
    [
        InlineKeyboardButton(text=BACK_BUTTON, callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}"),
    ],
    [
        InlineKeyboardButton(text='Home', callback_data="HONE"),
    ]
]
ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)
back_to_keyboard_markup = InlineKeyboardMarkup(back_to_keyboard)