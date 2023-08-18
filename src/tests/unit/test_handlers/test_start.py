from unittest.mock import AsyncMock, Mock, patch

import pytest
from telegram import MenuButtonCommands

from bot.constants.buttons import COMMANDS
from bot.constants.messages import START_MESSAGE
from bot.constants.states import States
from bot.handlers import main_handlers


@pytest.mark.asyncio
async def test_start_handler_response(update, context):
    """Start handler return correct response unittest."""
    reply_markup_mock = []
    context.bot.get_my_commands = AsyncMock(return_value=reply_markup_mock)
    with patch(
        "bot.handlers.main_handlers.build_assistance_keyboard",
        new=AsyncMock(return_value=[]),
    ):
        response = await main_handlers.start(update, context)
    assert response == States.ASSISTANCE, (
        f"Invalid state value, should be {States.ASSISTANCE}",
    )


@pytest.mark.parametrize("update_message", [True, False])
@pytest.mark.asyncio
async def test_start_handler_answer_to_user_message(
    update, context, update_message
):
    """Start handler return correct answer to user message unittest."""
    reply_markup_mock = []
    update.message = Mock() if update_message else None
    context.bot.get_my_commands = AsyncMock(return_value=reply_markup_mock)
    with patch(
        "bot.handlers.main_handlers.build_assistance_keyboard",
        new=AsyncMock(return_value=reply_markup_mock),
    ):
        await main_handlers.start(update, context)

    if update_message:
        update.message.reply_text.assert_called_once_with(
            START_MESSAGE, reply_markup=reply_markup_mock
        )
    else:
        query = update.callback_query
        query.answer.assert_called_once()
        query.edit_message_text.assert_called_once_with(
            START_MESSAGE, reply_markup=reply_markup_mock
        )


@pytest.mark.asyncio
async def test_start_handler_without_bot_commands(update, context):
    """Start handler get bot command correctly unittest."""
    context.bot.get_my_commands = AsyncMock(return_value=[])
    with patch(
        "bot.handlers.main_handlers.build_assistance_keyboard",
        new=AsyncMock(return_value=[]),
    ):
        await main_handlers.start(update, context)

    context.bot.set_my_commands.assert_called_once_with(commands=COMMANDS)
    context.bot.set_chat_menu_button.assert_called_once_with(
        menu_button=MenuButtonCommands()
    )
