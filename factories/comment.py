from typing import Any

from models.requests.comment import CreateCommentRequest
from utils.data_generators import DataGenerator


def create_comment_payload(post_id: int, **overrides: Any) -> CreateCommentRequest:
    data: dict[str, Any] = {
        "post_id": post_id,
        "name": DataGenerator.random_full_name(),
        "email": DataGenerator.random_email(),
        "body": DataGenerator.random_sentence(),
    }
    data.update(overrides)
    return CreateCommentRequest(**data)


def create_comment_payload_dict(post_id: int, **overrides: Any) -> dict[str, Any]:
    data = create_comment_payload(post_id).model_dump(mode="json")
    data.update(overrides)
    return data
