import random
from typing import Any

from models.requests.user import CreateUserRequest, UpdateUserRequest
from utils.data_generators import DataGenerator

GENDERS = ["male", "female"]


def create_user_payload(**overrides: Any) -> CreateUserRequest:
    data: dict[str, Any] = {
        "name": DataGenerator.random_full_name(),
        "email": DataGenerator.random_email(),
        "gender": random.choice(GENDERS),
        "status": "active",
    }
    data.update(overrides)
    return CreateUserRequest(**data)


def create_user_payload_dict(**overrides: Any) -> dict[str, Any]:
    data = create_user_payload().model_dump(mode="json")
    data.update(overrides)
    return data


def update_user_payload(**overrides: Any) -> UpdateUserRequest:
    data: dict[str, Any] = {
        "name": DataGenerator.random_full_name(),
        "status": "inactive",
    }
    data.update(overrides)
    return UpdateUserRequest(**data)
