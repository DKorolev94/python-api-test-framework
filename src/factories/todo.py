from typing import Any

from src.models.requests.todo import CreateTodoRequest, UpdateTodoRequest
from src.utils.data_generators import future_datetime, random_sentence


def create_todo_payload(user_id: int, **overrides: Any) -> CreateTodoRequest:
    """Собирает валидный запрос на создание задачи для позитивных тестов."""
    data: dict[str, Any] = {
        "user_id": user_id,
        "title": random_sentence(),
        "due_on": future_datetime(hours_ahead=24),
        "status": "pending",
    }
    data.update(overrides)
    return CreateTodoRequest(**data)


def create_todo_payload_dict(user_id: int, **overrides: Any) -> dict[str, Any]:
    """Собирает словарь с данными задачи для негативных тестов с некорректными данными."""
    data = create_todo_payload(user_id).model_dump(mode="json")
    data.update(overrides)
    return data


def update_todo_payload(**overrides: Any) -> UpdateTodoRequest:
    """Собирает валидный запрос на обновление задачи для позитивных тестов."""
    data: dict[str, Any] = {
        "title": random_sentence(),
        "status": "completed",
    }
    data.update(overrides)
    return UpdateTodoRequest(**data)
