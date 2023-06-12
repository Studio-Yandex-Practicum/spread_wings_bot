from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ASSISTANCE_BUTTON,
    BACK_BUTTON,
    CONTACTS,
    DONATION_BUTTON,
    SEND_REQUEST,
)
from bot.constants.regions import Regions
from bot.constants.states.main_states import States
from bot.constants.urls import DONATION_URL

assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=States.ASSISTANCE.value
        )
    ],
    [
        InlineKeyboardButton(text=DONATION_BUTTON, url=DONATION_URL),
    ],
]

region_keyboard = [
    [InlineKeyboardButton(region.value, callback_data=region.name)]
    for region in Regions
]

region_keyboard.append(
    [
        InlineKeyboardButton(
            BACK_BUTTON, callback_data=f"back_to_{States.ASSISTANCE.value}"
        )
    ]
)

contact_keyboard = [
    [
        InlineKeyboardButton(SEND_REQUEST, callback_data=States.BACK.value),
        InlineKeyboardButton(
            CONTACTS, callback_data=States.SHOW_CONTACTS.value
        ),
    ],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=States.REGION.value)],
]

contact_show_keyboard = [
    [InlineKeyboardButton(BACK_BUTTON, callback_data=States.CONTACT_US.value)]
]


assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)
region_keyboard_markup = InlineKeyboardMarkup(region_keyboard)
contact_keyboard_markup = InlineKeyboardMarkup(contact_keyboard)
contact_show_keyboard_markup = InlineKeyboardMarkup(contact_show_keyboard)
