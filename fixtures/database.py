from collections.abc import Generator

import pytest

from src.database.connectors.postgres_connector import DatabaseConnector, DatabaseManager
from src.database.queries.db_operations import DBOperation


@pytest.fixture
def db() -> Generator[DBOperation, None, None]:
    with DatabaseConnector() as connector:
        yield DBOperation(DatabaseManager(connector.connection))
