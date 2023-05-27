from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import ASSISTANCE_BUTTON, DONATION_BUTTON
from bot.constants.states import States

assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=States.ASSISTANCE
        ),
        InlineKeyboardButton(
            text=DONATION_BUTTON, callback_data=States.DONATION
        )
    ]
]

assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)


choose_region_keyboard = [
    [
        InlineKeyboardButton(
            text="Region 1", callback_data="test1"
        ),
        InlineKeyboardButton(
            text="Region 2", callback_data="test2"
        )
    ]
]

choose_region_keyboard_markup = InlineKeyboardMarkup(choose_region_keyboard)