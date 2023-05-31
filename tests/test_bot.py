# Здесь хранятся тесты бота
import pytest
from telegram import Bot
from telegram.error import InvalidToken


class TestBotWithoutRequest:
    """Withoutrequest."""

    async def test_no_token_passed(self):
        """Test no token pass."""
        with pytest.raises(InvalidToken, match="You must pass the token"):
            Bot("")
