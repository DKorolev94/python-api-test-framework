import allure
import pytest

from src.config.settings import settings
from src.utils.logger import configure_logging

configure_logging(level=settings.LOG_LEVEL)

pytest_plugins = [
    "fixtures.auth",
    "fixtures.database",
    "fixtures.user",
    "fixtures.post",
    "fixtures.comment",
    "fixtures.todo",
]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Добавляет каждому собранному тесту Allure метку и тег слоя 'api'."""
    for item in items:
        item.add_marker(allure.label("layer", "api"))
        item.add_marker(allure.tag("api"))


@pytest.fixture(scope="session")
def config():
    """Предоставляет тестам загруженные настройки приложения."""
    return settings
