from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import EMAIL, PHONE, TELEGRAM, BACK_BUTTON, HOME_BUTTON
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
        InlineKeyboardButton(text=BACK_BUTTON, callback_data=f"back_to_{States.SHOW_CONTACT.value}"),
    ],
]
back_to_keyboard.append(
    [
        InlineKeyboardButton(text=HOME_BUTTON,
                             callback_data=f"back_to_{States.ASSISTANCE.value}"),
    ]
)


back_to_question_keyboard = [
    [
        InlineKeyboardButton(text=BACK_BUTTON, callback_data=f"back_to_{States.ASK_QUESTION.value}"),
    ],
]
back_to_question_keyboard.append(
    [
        InlineKeyboardButton(text=HOME_BUTTON,
                             callback_data=f"back_to_{States.ASSISTANCE.value}"),
    ]
)


ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)
back_to_question_keyboard_markup = InlineKeyboardMarkup(back_to_question_keyboard)
back_to_keyboard_markup = InlineKeyboardMarkup(back_to_keyboard)