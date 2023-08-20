import pytest

from bot.constants.messages import HELP_MESSAGE
from bot.handlers import main_handlers


@pytest.mark.asyncio
async def test_help_handler(update, context):
    """Help handler unittest."""
    await main_handlers.help_command(update, context)
    update.message.reply_text.assert_called_once_with(HELP_MESSAGE)
