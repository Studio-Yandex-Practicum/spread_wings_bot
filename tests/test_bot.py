# Здесь хранятся тесты бота
import pytest
from telegram import Bot
from telegram.error import InvalidToken


class TestBotWithoutRequest:
    """Проверка бота без ответа."""

    async def test_no_token_passed(self):
        """Проверка наличия токена телеграмм."""
        with pytest.raises(InvalidToken, match="You must pass the token"):
            Bot("")
