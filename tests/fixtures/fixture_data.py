# Здесь хранятся необходимые фикстуры для тестов (в качестве примера)
from datetime import datetime

import pytest


@pytest.fixture
def current_timestamp():
    """Cur timestamp."""
    return datetime.now().timestamp()


@pytest.fixture
def main_url():
    """Url."""
    return "https://detskyfond.info/"
