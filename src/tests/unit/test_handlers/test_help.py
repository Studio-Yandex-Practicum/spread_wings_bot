from unittest.mock import AsyncMock, patch

import pytest
from telegram import InlineKeyboardMarkup

from bot.handlers import main_handlers
from bot.keyboards.assistance import (
    to_the_original_state_and_previous_step_keyboard,
)


@pytest.mark.asyncio
async def test_help_handler(
    update,
    context,
    mocked_message,
    mocked_message_text,
):
    """Help handler unittest."""
    help_back_button = InlineKeyboardMarkup(
        [to_the_original_state_and_previous_step_keyboard[0]]
    )

    with patch(
        "bot.handlers.assistance.BotSettings.objects.aget",
        AsyncMock(return_value=mocked_message),
    ):
        await main_handlers.help_command(update, context)
    update.message.reply_text.assert_called_once_with(
        mocked_message_text,
        reply_markup=help_back_button,
    )
