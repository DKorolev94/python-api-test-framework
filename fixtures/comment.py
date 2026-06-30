from typing import Generator

import pytest

from api.comments import CommentsAPI
from services.comment_service import CommentService


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
