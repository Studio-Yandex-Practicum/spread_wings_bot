from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import ASSISTANCE_BUTTON, DONATION_BUTTON
from bot.constants.states import States
from bot.constants.regions import Regions


assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=States.REGION
        ),
        InlineKeyboardButton(
            text=DONATION_BUTTON, callback_data=States.DONATION
        )
    ]
]

assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)

choose_region_keyboard = [[InlineKeyboardButton(region.value, callback_data=region)] for region in Regions]
choose_region_keyboard_markup = InlineKeyboardMarkup(choose_region_keyboard)