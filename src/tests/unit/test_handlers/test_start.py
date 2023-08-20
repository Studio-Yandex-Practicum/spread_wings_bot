from unittest.mock import AsyncMock, Mock, patch

import pytest
from telegram import MenuButtonCommands

from bot.constants.buttons import COMMANDS
from bot.constants.states import States
from bot.handlers import main_handlers


@pytest.mark.asyncio
async def test_start_handler_response(
    update,
    context,
    mocked_reply_markup,
    mocked_message,
):
    """Start handler return correct response unittest."""
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)
    with (
        patch(
            "bot.handlers.main_handlers.build_assistance_keyboard",
            new=AsyncMock(return_value=[]),
        ),
        patch(
            "bot.handlers.main_handlers.BotSettings.objects.aget",
            AsyncMock(return_value=mocked_message),
        ),
    ):
        response = await main_handlers.start(update, context)
    assert response == States.ASSISTANCE, (
        f"Invalid state value, should be {States.ASSISTANCE}",
    )


@pytest.mark.parametrize("update_message", [True, False])
@pytest.mark.asyncio
async def test_start_handler_answer_to_user_message(
    update,
    context,
    mocked_reply_markup,
    mocked_message,
    mocked_message_text,
    update_message,
):
    """Start handler return correct answer to user message unittest."""
    update.message = Mock() if update_message else None
    context.bot.get_my_commands = AsyncMock(return_value=mocked_reply_markup)
    with (
        patch(
            "bot.handlers.main_handlers.build_assistance_keyboard",
            new=AsyncMock(return_value=mocked_reply_markup),
        ),
        patch(
            "bot.handlers.main_handlers.BotSettings.objects.aget",
            AsyncMock(return_value=mocked_message),
        ),
    ):
        await main_handlers.start(update, context)

    if update_message:
        update.message.reply_text.assert_called_once_with(
            mocked_message_text, reply_markup=mocked_reply_markup
        )
    else:
        query = update.callback_query
        query.answer.assert_called_once()
        query.edit_message_text.assert_called_once_with(
            mocked_message_text, reply_markup=mocked_reply_markup
        )


@pytest.mark.asyncio
async def test_start_handler_without_bot_commands(
    update,
    context,
    mocked_message,
):
    """Start handler get bot command correctly unittest."""
    context.bot.get_my_commands = AsyncMock(return_value=[])
    with (
        patch(
            "bot.handlers.main_handlers.build_assistance_keyboard",
            new=AsyncMock(return_value=[]),
        ),
        patch(
            "bot.handlers.main_handlers.BotSettings.objects.aget",
            AsyncMock(return_value=mocked_message),
        ),
    ):
        await main_handlers.start(update, context)

    context.bot.set_my_commands.assert_called_once_with(commands=COMMANDS)
    context.bot.set_chat_menu_button.assert_called_once_with(
        menu_button=MenuButtonCommands()
    )
