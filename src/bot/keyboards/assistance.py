from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.buttons import (ASSISTANCE_BUTTON,
                                   BACK_BUTTON,
                                   DONATION_BUTTON)
from bot.constants.states import HELP, GET_HELP, BACK
from bot.constants.urls import DONATION_URL


assistance_keyboard = [
    [
        InlineKeyboardButton(
            text=ASSISTANCE_BUTTON, callback_data=GET_HELP
        ),
        InlineKeyboardButton(
            text=DONATION_BUTTON, callback_data=HELP
        )
    ]
]

donation_keyboard = [
    [InlineKeyboardButton(DONATION_BUTTON, url=DONATION_URL)],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK)]
]

donation_keyboard_markup = InlineKeyboardMarkup(donation_keyboard)
assistance_keyboard_markup = InlineKeyboardMarkup(assistance_keyboard)

# для теста в последствии удалить или перенести в клавиатуру выбора регионов
region_keyboard = [
    [
        InlineKeyboardButton('Москва', callback_data='moscow'),
        InlineKeyboardButton('Самара', callback_data='samara')
    ],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK)]
]
region_keyboard_markup = InlineKeyboardMarkup(region_buttons)
