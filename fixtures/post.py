from typing import Generator

import pytest

from api.posts import PostsAPI
from factories.post import create_post_payload
from models.responses.post import PostResponse
from models.responses.user import UserResponse
from services.post_service import PostService


@pytest.fixture
def posts_api(api_token: str) -> Generator[PostsAPI, None, None]:
    with PostsAPI(token=api_token) as api:
        yield api


@pytest.fixture
def posts_api_no_auth() -> Generator[PostsAPI, None, None]:
    with PostsAPI(token=None) as api:
        yield api


@pytest.fixture
def post_service(posts_api: PostsAPI) -> PostService:
    return PostService(posts_api)


@pytest.fixture
def created_post(
    post_service: PostService, created_user: UserResponse
) -> Generator[PostResponse, None, None]:
    post = post_service.create_post(create_post_payload(user_id=created_user.id))
    yield post
    post_service.delete_post(post.id)
