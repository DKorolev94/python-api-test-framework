from typing import Any

from models.requests.todo import CreateTodoRequest, UpdateTodoRequest
from utils.data_generators import DataGenerator


def create_todo_payload(user_id: int, **overrides: Any) -> CreateTodoRequest:
    data: dict[str, Any] = {
        "user_id": user_id,
        "title": DataGenerator.random_sentence(),
        "due_on": DataGenerator.future_datetime(hours_ahead=24),
        "status": "pending",
    }
    data.update(overrides)
    return CreateTodoRequest(**data)


def create_todo_payload_dict(user_id: int, **overrides: Any) -> dict[str, Any]:
    data = create_todo_payload(user_id).model_dump(mode="json")
    data.update(overrides)
    return data


def update_todo_payload(**overrides: Any) -> UpdateTodoRequest:
    data: dict[str, Any] = {
        "title": DataGenerator.random_sentence(),
        "status": "completed",
    }
    data.update(overrides)
    return UpdateTodoRequest(**data)
