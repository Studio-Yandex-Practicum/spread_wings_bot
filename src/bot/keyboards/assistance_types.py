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
from bot.models import HelpTypes

assistance_types_keyboard = [
    [
        InlineKeyboardButton(
            text=LEGAL_HELP_BUTTON,
            callback_data=HelpTypes.LEGAL_ASSISTANCE,
        )
    ],
    [
        InlineKeyboardButton(
            text=SOCIAL_HELP_BUTTON,
            callback_data=HelpTypes.SOCIAL_ASSISTANCE,
        )
    ],
    [
        InlineKeyboardButton(
            text=PSYCHOLOGICAL_HELP_BUTTON,
            callback_data=HelpTypes.PSYCHOLOGICAL_ASSISTANCE,
        )
    ],
    [
        InlineKeyboardButton(
            text=PROGRAMS_BUTTON,
            callback_data=States.FUND_PROGRAMS.value,
        )
    ],
    [
        InlineKeyboardButton(
            text=CONTACT_US_BUTTON,
            callback_data=States.CONTACT_US.value,
        )
    ],
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE.value}",
        )
    ],
]

assistance_types_keyboard_markup = InlineKeyboardMarkup(
    assistance_types_keyboard,
)
