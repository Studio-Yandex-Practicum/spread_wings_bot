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
