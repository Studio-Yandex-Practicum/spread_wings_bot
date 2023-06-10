# Здесь хранятся необходимые фикстуры для тестов (в качестве примера)
from datetime import datetime

import pytest


@pytest.fixture
def current_timestamp() -> datetime:
    """Возвращаем текущее время."""

    return datetime.now().timestamp()


@pytest.fixture
def main_url() -> str:
    """Возвращаем основной путь."""

    return "https://detskyfond.info/"
