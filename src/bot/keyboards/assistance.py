import re
from typing import Tuple, Optional

from async_lru import alru_cache
from django.conf import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.core.paginator import Paginator

from bot.constants.buttons import (
    ASK_QUESTION,
    ASSISTANCE_BUTTON,
    BACK_BUTTON,
    CONTACTS,
    DONATION_BUTTON,
)
from bot.constants.patterns import PARSE_CALLBACK_DATA, PAGE_SEP_SYMBOL
from bot.constants.states.main_states import States
from bot.keyboards.utils.telegram_pagination import InlineKeyboardPaginator
from bot.models import Question
from bot_settings.models import BotSettings
from core.models import Region
from asgiref.sync import sync_to_async

QUESTIONS_PER_PAGE = 6


# uncomment the line if we actually need to cache this keyboard
# @alru_cache(ttl=settings.KEYBOARDS_CACHE_TTL)
async def build_assistance_keyboard() -> InlineKeyboardMarkup:
    """
    Build telegram assistance keyboard async.
    After building cache it.
    """
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
                InlineKeyboardButton(text=DONATION_BUTTON,
                                     url=setting.value),
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


@alru_cache(ttl=settings.KEYBOARDS_CACHE_TTL)
async def build_question_keyboard(
        region: str,
        question_type: str,
        page: int,
) -> InlineKeyboardMarkup:
    """
    Build telegram assistance questions keyboard async.
    After building cache it.
    """
    queryset = await sync_to_async(list)(Question.objects.filter(
        regions__region_key=region,
        question_type=question_type,
    ).values("id", "short_description"))
    data_paginator = Paginator(queryset, QUESTIONS_PER_PAGE)
    telegram_paginator = InlineKeyboardPaginator(
        data_paginator.num_pages,
        current_page=page,
        data_pattern=''.join([question_type, PAGE_SEP_SYMBOL, '{page}']),
    )
    for question in data_paginator.page(page):
        telegram_paginator.add_before(
            InlineKeyboardButton(
                text=question.get("short_description"),
                callback_data=question.get("id"),
            )
        )
    telegram_paginator.add_after(
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}",
        ),
        InlineKeyboardButton(
            text=ASK_QUESTION,
            callback_data=States.ASK_QUESTION.value,
        ),
    )
    return telegram_paginator


def parse_callback_data(
        callback_data: str,
) -> Tuple[Optional[str], Optional[int]]:
    """
    Parse callback data to get page number and
    question type for pagination.
    """
    match = re.match(PARSE_CALLBACK_DATA, callback_data)
    if match:
        question_type, page_number = match.groups()
        page_number = int(page_number) if page_number is not None else None
        return question_type, page_number
    return None, None


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
