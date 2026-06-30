from typing import Generator

import pytest

from api.todos import TodosAPI
from services.todo_service import TodoService


@pytest.fixture
def todos_api(api_token: str) -> Generator[TodosAPI, None, None]:
    with TodosAPI(token=api_token) as api:
        yield api


@pytest.fixture
def todos_api_no_auth() -> Generator[TodosAPI, None, None]:
    with TodosAPI(token=None) as api:
        yield api


@pytest.fixture
def todo_service(todos_api: TodosAPI) -> TodoService:
    return TodoService(todos_api)
