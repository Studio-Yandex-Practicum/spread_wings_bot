from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    BACK_BUTTON,
    CONTACT_US_BUTTON,
    LEGAL_HELP_BUTTON,
    PROGRAMS_BUTTON,
    PSYCHOLOGICAL_HELP_BUTTON,
    SOCIAL_HELP_BUTTON,
)
from bot.constants.states import States

assistance_types_keyboard = [
    [
        InlineKeyboardButton(
            text=LEGAL_HELP_BUTTON, callback_data=States.LEGAL_ASSISTANCE.value
        ),
        InlineKeyboardButton(
            text=SOCIAL_HELP_BUTTON,
            callback_data=States.SOCIAL_ASSISTANCE.value,
        ),
        InlineKeyboardButton(
            text=PSYCHOLOGICAL_HELP_BUTTON,
            callback_data=States.PSYCHOLOGICAL_ASSISTANCE.value,
        ),
    ],
    [
        InlineKeyboardButton(
            text=PROGRAMS_BUTTON, callback_data=States.FUND_PROGRAMS.value
        ),
        InlineKeyboardButton(
            text=CONTACT_US_BUTTON, callback_data=States.CONTACT_US.value
        ),
    ],
    [
        InlineKeyboardButton(
            text=BACK_BUTTON, callback_data=f"back_to_{States.REGION.value}"
        )
    ],
]

assistance_types_keyboard_markup = InlineKeyboardMarkup(
    assistance_types_keyboard
)
