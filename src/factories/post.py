from typing import Any

from src.models.requests.post import CreatePostRequest, UpdatePostRequest
from src.utils.data_generators import random_paragraph, random_sentence


def create_post_payload(user_id: int, **overrides: Any) -> CreatePostRequest:
    """Собирает валидный запрос на создание поста для позитивных тестов."""
    data: dict[str, Any] = {
        "user_id": user_id,
        "title": random_sentence(),
        "body": random_paragraph(),
    }
    data.update(overrides)
    return CreatePostRequest(**data)


def create_post_payload_dict(user_id: int, **overrides: Any) -> dict[str, Any]:
    """Собирает словарь с данными поста для негативных тестов с некорректными данными."""
    data = create_post_payload(user_id).model_dump(mode="json")
    data.update(overrides)
    return data


def update_post_payload(**overrides: Any) -> UpdatePostRequest:
    """Собирает валидный запрос на обновление поста для позитивных тестов."""
    data: dict[str, Any] = {
        "title": random_sentence(),
        "body": random_paragraph(),
    }
    data.update(overrides)
    return UpdatePostRequest(**data)
