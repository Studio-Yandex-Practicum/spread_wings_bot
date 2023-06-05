from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ASK_QUESTION,
    BACK_BUTTON,
    CONTACT_US_BUTTON,
    LEGAL_HELP_BUTTON,
    PROGRAMS_BUTTON,
    PSYCHOLOGICAL_HELP_BUTTON,
    SOCIAL_HELP_BUTTON,
)
from bot.constants.list_of_questions import LegalQuestions
from bot.constants.states.main_states import States

assistance_types_keyboard = [
    [
        InlineKeyboardButton(
            text=LEGAL_HELP_BUTTON, callback_data="assistance_type_legal"
        ),
        InlineKeyboardButton(
            text=SOCIAL_HELP_BUTTON, callback_data="assistance_type_social"
        ),
        InlineKeyboardButton(
            text=PSYCHOLOGICAL_HELP_BUTTON,
            callback_data="assistance_type_psychological",
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

assistance_questions_keyboard = [
    [InlineKeyboardButton(question.value, callback_data=question.name)]
    for question in LegalQuestions
]

assistance_questions_keyboard.append(
    [
        InlineKeyboardButton(
            text=ASK_QUESTION, callback_data=States.ASK_QUESTION.value
        )
    ]
)

assistance_questions_keyboard.append(
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}",
        )
    ]
)


assistance_types_keyboard_markup = InlineKeyboardMarkup(
    assistance_types_keyboard
)

assistance_questions_keyboard_markup = InlineKeyboardMarkup(
    assistance_questions_keyboard
)
