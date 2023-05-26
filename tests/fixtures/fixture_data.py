# Здесь хранятся необходимые фикстуры для тестов (в качестве примера)
from datetime import datetime

import pytest


@pytest.fixture
def current_timestamp():
    return datetime.now().timestamp()


@pytest.fixture
def main_url():
    return 'https://detskyfond.info/'
