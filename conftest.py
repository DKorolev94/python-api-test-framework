import pytest

from config.settings import settings
from utils.logger import configure_logging

configure_logging(level=settings.LOG_LEVEL)

pytest_plugins = [
    "fixtures.auth",
    "fixtures.user",
    "fixtures.post",
    "fixtures.comment",
    "fixtures.todo",
]


@pytest.fixture(scope="session")
def config():
    return settings
