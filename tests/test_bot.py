# Здесь хранятся тесты бота
import pytest
from telegram import Bot
from telegram.error import InvalidToken


class TestBotWithoutRequest:
    async def test_no_token_passed(self):
        with pytest.raises(InvalidToken, match="You must pass the token"):
            Bot("")
