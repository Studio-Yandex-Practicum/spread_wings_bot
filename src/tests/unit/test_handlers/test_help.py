from unittest.mock import AsyncMock, patch

import pytest

from bot.handlers import main_handlers


@pytest.mark.asyncio
async def test_help_handler(
    update,
    context,
    mocked_message,
    mocked_message_text,
):
    """Help handler unittest."""
    with patch(
        "bot.handlers.assistance.BotSettings.objects.aget",
        AsyncMock(return_value=mocked_message),
    ):
        await main_handlers.help_command(update, context)
    update.message.reply_text.assert_called_once_with(mocked_message_text)
