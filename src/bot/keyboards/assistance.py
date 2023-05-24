from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants import (ASSISTANCE,
                           BACK,
                           DONATION,
                           DONATION_BUTTON,
                           DONATION_URL,
                           ASSISTANCE_BUTTON,
                           BACK_BUTTON)


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

donation_button = [
    [InlineKeyboardButton(DONATION_BUTTON, url=DONATION_URL)],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK)]
]

donation = InlineKeyboardMarkup(donation_button)
assistance = InlineKeyboardMarkup(assistance_keyboard)

# для теста в последствии удалить или перенести в клавиатуру выбора регионов
region_buttons = [
    [
        InlineKeyboardButton('Москва', callback_data='moscow'),
        InlineKeyboardButton('Самара', callback_data='samara')
    ],
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK)]
]
region = InlineKeyboardMarkup(region_buttons)
