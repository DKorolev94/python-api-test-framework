from typing import Any

from models.requests.post import CreatePostRequest, UpdatePostRequest
from utils.data_generators import DataGenerator


def create_post_payload(user_id: int, **overrides: Any) -> CreatePostRequest:
    data: dict[str, Any] = {
        "user_id": user_id,
        "title": DataGenerator.random_sentence(),
        "body": DataGenerator.random_paragraph(),
    }
    data.update(overrides)
    return CreatePostRequest(**data)


def create_post_payload_dict(user_id: int, **overrides: Any) -> dict[str, Any]:
    data = create_post_payload(user_id).model_dump(mode="json")
    data.update(overrides)
    return data


def update_post_payload(**overrides: Any) -> UpdatePostRequest:
    data: dict[str, Any] = {
        "title": DataGenerator.random_sentence(),
        "body": DataGenerator.random_paragraph(),
    }
    data.update(overrides)
    return UpdatePostRequest(**data)
