from unittest.mock import AsyncMock, patch

import pytest

from bot.constants.states import States
from bot.handlers.assistance import receive_assistance


@pytest.mark.asyncio
async def test_receive_assistance(
    update,
    context,
    mocked_reply_markup,
    mocked_message,
    mocked_message_text,
):
    """Receive assistance handler unittest."""
    with (
        patch(
            "bot.handlers.assistance.build_region_keyboard",
            AsyncMock(return_value=mocked_reply_markup),
        ),
        patch(
            "bot.handlers.assistance.BotSettings.objects.aget",
            AsyncMock(return_value=mocked_message),
        ),
    ):
        response = await receive_assistance(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with(
        text=mocked_message_text, reply_markup=mocked_reply_markup
    )
    assert response == States.REGION, (
        f"Invalid state value, should be {States.REGION}",
    )
