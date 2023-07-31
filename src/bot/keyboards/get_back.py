from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import BACK_BUTTON


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура кнопки назад."""
    back_button_inline_keyboard = [
        [InlineKeyboardButton(BACK_BUTTON, callback_data="back")]
    ]
    return InlineKeyboardMarkup(back_button_inline_keyboard)
