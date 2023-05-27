from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.buttons import (ASSISTANCE_BUTTON,
                                   BACK_BUTTON,
                                   DONATION_BUTTON)
from bot.constants.states import States
from bot.constants.regions import Regions
from bot.constants.urls import DONATION_URL


assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=States.ASSISTANCE.value
        ),
        InlineKeyboardButton(
            text=DONATION_BUTTON, callback_data=States.DONATION.value
        )
    ]
]

donation_keyboard = [
    [InlineKeyboardButton(DONATION_BUTTON, url=DONATION_URL)],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=States.BACK.value)]
]

donation_keyboard_markup = InlineKeyboardMarkup(donation_keyboard)
assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)

region_keyboard = [[InlineKeyboardButton(region.value, callback_data=region)] for region in Regions]
region_keyboard.append([InlineKeyboardButton(BACK_BUTTON, callback_data=States.BACK.value)])
region_keyboard_markup = InlineKeyboardMarkup(region_keyboard)