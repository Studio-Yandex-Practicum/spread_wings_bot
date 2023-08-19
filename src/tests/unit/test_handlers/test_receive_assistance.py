from unittest.mock import AsyncMock, patch

import pytest

from bot.constants.messages import ASSISTANCE_MESSAGE
from bot.constants.states import States
from bot.handlers.assistance import receive_assistance


@pytest.mark.asyncio
async def test_receive_assistance(update, context):
    """Receive assistance handler unittest."""
    keyboard = []

    with patch(
        "bot.handlers.assistance.build_region_keyboard",
        AsyncMock(return_value=keyboard),
    ):
        response = await receive_assistance(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with(
        text=ASSISTANCE_MESSAGE, reply_markup=keyboard
    )
    assert response == States.REGION, (
        f"Invalid state value, should be {States.REGION}",
    )
