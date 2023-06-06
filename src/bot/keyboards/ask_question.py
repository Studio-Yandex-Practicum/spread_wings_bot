from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import EMAIL, PHONE, TELEGRAM

ask_question_keyboard = [
    [
        InlineKeyboardButton(text=EMAIL, callback_data="EMAIL"),
        InlineKeyboardButton(text=PHONE, callback_data="PHONE"),
        InlineKeyboardButton(text=TELEGRAM, callback_data="TELEGRAM"),
    ]
]

ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)
