from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import ASSISTANCE_BUTTON, DONATION_BUTTON
from bot.constants.states import ASSISTANCE, DONATION

assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=ASSISTANCE
        ),
        InlineKeyboardButton(
            text=DONATION_BUTTON, callback_data=DONATION
        )
    ]
]

assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)
