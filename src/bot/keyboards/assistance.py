from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ASK_QUESTION,
    ASSISTANCE_BUTTON,
    BACK_BUTTON,
    CONTACTS,
    DONATION_BUTTON,
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

assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)

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

region_keyboard_markup = InlineKeyboardMarkup(region_keyboard)

contact_type_keyboard = [
    [
        InlineKeyboardButton(
            ASK_QUESTION, callback_data=States.ASK_QUESTION.value
        ),
    ],
    [
        InlineKeyboardButton(
            CONTACTS, callback_data=States.SHOW_CONTACT.value
        ),
    ],
    [
        InlineKeyboardButton(
            BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}",
        )
    ],
]

contact_type_keyboard_markup = InlineKeyboardMarkup(contact_type_keyboard)

contact_show_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.CONTACT_US.value}",
        )
    ]
]

contact_show_keyboard_markup = InlineKeyboardMarkup(contact_show_keyboard)
