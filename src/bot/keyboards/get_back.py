from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import BACK_BUTTON
from bot.constants.states.main_states import States


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура кнопки назад."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=BACK_BUTTON,
                    callback_data=f"back_to_{States.ASSISTANCE.value}",
                )
            ],
        ]
    )
