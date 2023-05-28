from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ASSISTANCE_BUTTON,
    BACK_BUTTON,
    DONATION_BUTTON,
)
from bot.constants.states import States
from bot.constants.urls import DONATION_URL

assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=States.ASSISTANCE.value
        ),
        InlineKeyboardButton(text=DONATION_BUTTON, url=DONATION_URL),
    ]
]

assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)

# для теста в последствии удалить или перенести в клавиатуру выбора регионов
region_keyboard = [
    [
        InlineKeyboardButton('Москва', callback_data='moscow'),
        InlineKeyboardButton('Самара', callback_data='samara'),
    ],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=States.BACK.value)],
]
region_keyboard_markup = InlineKeyboardMarkup(region_keyboard)
