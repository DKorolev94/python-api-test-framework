from typing import Any

from src.models.requests.comment import CreateCommentRequest
from src.utils.data_generators import random_email, random_full_name, random_sentence


def create_comment_payload(post_id: int, **overrides: Any) -> CreateCommentRequest:
    """Собирает валидный запрос на создание комментария для позитивных тестов."""
    data: dict[str, Any] = {
        "post_id": post_id,
        "name": random_full_name(),
        "email": random_email(),
        "body": random_sentence(),
    }
    data.update(overrides)
    return CreateCommentRequest(**data)


def create_comment_payload_dict(post_id: int, **overrides: Any) -> dict[str, Any]:
    """Собирает словарь с данными комментария для негативных тестов с некорректными данными."""
    data = create_comment_payload(post_id).model_dump(mode="json")
    data.update(overrides)
    return data
