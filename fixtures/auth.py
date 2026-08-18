import pytest

from src.config.settings import settings


@pytest.fixture(scope="session")
def api_token() -> str:
    """Bearer token from GOREST_TOKEN env var."""
    return settings.GOREST_TOKEN
