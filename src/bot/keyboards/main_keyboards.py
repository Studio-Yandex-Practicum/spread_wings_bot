from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants import Regions


class Kboards():

    def choosing_region_keybord():
        keyboard_buttons = []
        for region in list(Regions):
            keyboard_buttons.append([InlineKeyboardButton(region.value, callback_data=region)])
        inline_keyboard = InlineKeyboardMarkup(keyboard_buttons)
        return inline_keyboard