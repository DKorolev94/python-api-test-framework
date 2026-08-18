from collections.abc import Generator

import pytest

from src.api.clients.comments import CommentsAPI
from src.api.services.comment_service import CommentService
from src.factories.comment import create_comment_payload
from src.models.responses.comment import CommentResponse
from src.models.responses.post import PostResponse


@pytest.fixture
def comments_api(api_token: str) -> Generator[CommentsAPI, None, None]:
    with CommentsAPI(token=api_token) as api:
        yield api


@pytest.fixture
def comments_api_no_auth() -> Generator[CommentsAPI, None, None]:
    with CommentsAPI(token=None) as api:
        yield api


@pytest.fixture
def comment_service(comments_api: CommentsAPI) -> CommentService:
    return CommentService(comments_api)


@pytest.fixture
def created_comment(
    comment_service: CommentService, created_post: PostResponse
) -> Generator[CommentResponse, None, None]:
    comment = comment_service.create_comment(create_comment_payload(post_id=created_post.id))
    yield comment
    comment_service.delete_comment(comment.id)
