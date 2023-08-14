from async_lru import alru_cache
from django.conf import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ASK_QUESTION,
    ASSISTANCE_BUTTON,
    BACK_BUTTON,
    BACK_TO_START_BUTTON,
    CONTACTS,
    DONATION_BUTTON,
)
from bot.constants.states.main_states import States
from bot_settings.models import BotSettings
from core.models import Region


# uncomment the line if we actually need to cache this keyboard
# @alru_cache(ttl=settings.KEYBOARDS_CACHE_TTL)
async def build_assistance_keyboard() -> InlineKeyboardMarkup:
    """Build telegram assistance keyboard async. After building cache it."""
    setting = await BotSettings.objects.aget(key="donation_url")
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=ASSISTANCE_BUTTON,
                    callback_data=States.ASSISTANCE.value,
                )
            ],
            [
                InlineKeyboardButton(text=DONATION_BUTTON, url=setting.value),
            ],
        ]
    )


@alru_cache(ttl=settings.KEYBOARDS_CACHE_TTL)
async def build_region_keyboard() -> InlineKeyboardMarkup:
    """
    Build telegram assistance type keyboard async.

    After building cache it.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=region.region_name,
                callback_data=region.region_key,
            )
        ]
        async for region in Region.objects.all()
    ]
    back_button = [
        [
            InlineKeyboardButton(
                text=BACK_BUTTON,
                callback_data=f"back_to_{States.ASSISTANCE.value}",
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard + back_button)


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

to_the_original_state_and_previous_step_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_TO_START_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE.value}",
        )
    ],
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.CONTACT_US.value}",
        )
    ],
]

to_the_original_state_and_previous_step_keyboard_markup = InlineKeyboardMarkup(
    to_the_original_state_and_previous_step_keyboard
)
