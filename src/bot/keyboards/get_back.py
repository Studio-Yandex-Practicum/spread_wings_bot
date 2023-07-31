from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import BACK_BUTTON


def get_back_keyboard(previous_state=None) -> InlineKeyboardMarkup:
    """Build the inline keyboard with a 'Back' button."""
    back_button_inline_keyboard = [
        [
            InlineKeyboardButton(
                BACK_BUTTON, callback_data=f"back_to_{previous_state}"
            )
        ]
    ]
    return InlineKeyboardMarkup(back_button_inline_keyboard)
