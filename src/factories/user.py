import random
from typing import Any

from src.models.requests.user import CreateUserRequest, UpdateUserRequest
from src.utils.data_generators import random_email, random_full_name

GENDERS = ["male", "female"]


def create_user_payload(**overrides: Any) -> CreateUserRequest:
    """Собирает валидный запрос на создание пользователя для позитивных тестов."""
    data: dict[str, Any] = {
        "name": random_full_name(),
        "email": random_email(),
        "gender": random.choice(GENDERS),
        "status": "active",
    }
    data.update(overrides)
    return CreateUserRequest(**data)


def create_user_payload_dict(**overrides: Any) -> dict[str, Any]:
    """Собирает словарь с данными пользователя для негативных тестов с некорректными данными."""
    data = create_user_payload().model_dump(mode="json")
    data.update(overrides)
    return data


def update_user_payload(**overrides: Any) -> UpdateUserRequest:
    """Собирает валидный запрос на обновление пользователя для позитивных тестов."""
    data: dict[str, Any] = {
        "name": random_full_name(),
        "status": "inactive",
    }
    data.update(overrides)
    return UpdateUserRequest(**data)
