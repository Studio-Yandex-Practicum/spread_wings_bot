from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ASSISTANCE_BUTTON,
    BACK_BUTTON,
    BACK_TO_START_BUTTON,
    CONTACTS,
    DONATION_BUTTON,
    GET_USER_QUESTION,
)
from bot.constants.patterns import PAGE_SEP_SYMBOL
from bot.constants.states import States
from bot.keyboards.utils.telegram_pagination import InlineKeyboardPaginator
from bot.models import FundProgram, Question
from bot_settings.models import BotSettings
from core.models import Region

PROGRAMS_PER_PAGE = 6
QUESTIONS_PER_PAGE = 6


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
                    callback_data=States.GET_ASSISTANCE.value,
                )
            ],
            [
                InlineKeyboardButton(text=DONATION_BUTTON, url=setting.value),
            ],
        ]
    )


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
                callback_data=f"back_to_{States.GET_ASSISTANCE.value}",
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard + back_button)


async def build_question_keyboard(
    region: str,
    question_type: str,
    page: int,
) -> InlineKeyboardPaginator:
    """
    Build telegram assistance questions keyboard async.

    After building cache it.
    """
    queryset = await sync_to_async(list)(
        Question.objects.filter(
            regions__region_key=region,
            question_type=question_type,
        ).values("id", "short_description")
    )
    data_paginator = Paginator(queryset, QUESTIONS_PER_PAGE)
    telegram_paginator = InlineKeyboardPaginator(
        data_paginator.num_pages,
        current_page=page,
        data_pattern="".join([question_type, PAGE_SEP_SYMBOL, "{page}"]),
    )
    for question in data_paginator.page(page):
        telegram_paginator.add_before(
            InlineKeyboardButton(
                text=question.get("short_description"),
                callback_data="".join(
                    [
                        States.SHOW_QUESTION.value,
                        PAGE_SEP_SYMBOL,
                        str(question.get("id")),
                    ]
                ),
            )
        )
    telegram_paginator.add_after(
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}",
        ),
        InlineKeyboardButton(
            text=GET_USER_QUESTION,
            callback_data=States.GET_USER_QUESTION.value,
        ),
    )
    return telegram_paginator


async def build_fund_program_keyboard(
    region: str,
    page: int,
) -> InlineKeyboardPaginator:
    """
    Build telegram assistance questions keyboard async.

    After building cache it.
    """
    queryset = await sync_to_async(list)(
        FundProgram.objects.filter(
            regions__region_key=region,
        ).values("id", "short_description")
    )
    data_paginator = Paginator(queryset, PROGRAMS_PER_PAGE)
    telegram_paginator = InlineKeyboardPaginator(
        data_paginator.num_pages,
        current_page=page,
        data_pattern="".join(
            [States.FUND_PROGRAMS.value, PAGE_SEP_SYMBOL, "{page}"]
        ),
    )
    for program in data_paginator.page(page):
        telegram_paginator.add_before(
            InlineKeyboardButton(
                text=program.get("short_description"),
                callback_data="".join(
                    [
                        States.SHOW_PROGRAM.value,
                        PAGE_SEP_SYMBOL,
                        str(program.get("id")),
                    ]
                ),
            )
        )
    telegram_paginator.add_after(
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.ASSISTANCE_TYPE.value}",
        ),
        InlineKeyboardButton(
            text=GET_USER_QUESTION,
            callback_data=States.GET_USER_QUESTION.value,
        ),
    )
    return telegram_paginator


contact_type_keyboard = [
    [
        InlineKeyboardButton(
            GET_USER_QUESTION, callback_data=States.GET_USER_QUESTION.value
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

show_fund_program_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.FUND_PROGRAMS.value}",
        ),
        InlineKeyboardButton(
            GET_USER_QUESTION, callback_data=States.GET_USER_QUESTION.value
        ),
    ]
]
show_fund_program_keyboard_markup = InlineKeyboardMarkup(
    show_fund_program_keyboard
)

question_show_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_BUTTON,
            callback_data=f"back_to_{States.SHOW_QUESTION.value}",
        )
    ]
]
question_show_keyboard_markup = InlineKeyboardMarkup(question_show_keyboard)

to_the_original_state_and_previous_step_keyboard = [
    [
        InlineKeyboardButton(
            text=BACK_TO_START_BUTTON,
            callback_data=f"back_to_{States.GET_ASSISTANCE.value}",
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
