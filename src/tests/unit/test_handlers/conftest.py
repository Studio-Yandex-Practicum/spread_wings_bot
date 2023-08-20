from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def update():
    """Update object fixture for telegram handlers."""
    return AsyncMock()


@pytest.fixture
def context():
    """Context object fixture for telegram handlers."""
    context = AsyncMock()
    context.bot = Mock()
    context.bot.set_my_commands = AsyncMock(return_value=[])
    context.bot.set_chat_menu_button = AsyncMock(return_value=[])
    return context


@pytest.fixture
def mocked_reply_markup():
    """Reply markup mock."""
    return []


@pytest.fixture
def mocked_message_text():
    """Message text mock."""
    return "MESSAGE"


@pytest.fixture
def mocked_message(mocked_message_text):
    """Message object mock."""
    message = Mock()
    message.value = mocked_message_text
    return message
