from collections.abc import Generator

import pytest

from src.api.clients.todos import TodosAPI
from src.api.services.todo_service import TodoService
from src.factories.todo import create_todo_payload
from src.models.responses.todo import TodoResponse
from src.models.responses.user import UserResponse


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


@pytest.fixture
def created_todo(
    todo_service: TodoService, created_user: UserResponse
) -> Generator[TodoResponse, None, None]:
    todo = todo_service.create_todo(create_todo_payload(user_id=created_user.id))
    yield todo
    todo_service.delete_todo(todo.id)
