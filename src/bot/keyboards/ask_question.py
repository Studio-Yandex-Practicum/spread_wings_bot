from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import EMAIL, PHONE, TELEGRAM

ask_question_keyboard = [
    [
        InlineKeyboardButton(text=EMAIL, callback_data="contact_EMAIL"),
        InlineKeyboardButton(text=PHONE, callback_data="contact_PHONE"),
        InlineKeyboardButton(text=TELEGRAM, callback_data="contact_TELEGRAM"),
    ]
]

ask_question_keyboard_markup = InlineKeyboardMarkup(ask_question_keyboard)
