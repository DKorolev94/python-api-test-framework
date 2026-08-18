from collections.abc import Generator

import pytest

from src.api.clients.users import UsersAPI
from src.api.services.user_service import UserService
from src.factories.user import create_user_payload
from src.models.responses.user import UserResponse


@pytest.fixture
def users_api(api_token: str) -> Generator[UsersAPI, None, None]:
    with UsersAPI(token=api_token) as api:
        yield api


@pytest.fixture
def users_api_no_auth() -> Generator[UsersAPI, None, None]:
    with UsersAPI(token=None) as api:
        yield api


@pytest.fixture
def user_service(users_api: UsersAPI) -> UserService:
    return UserService(users_api)


@pytest.fixture
def created_user(user_service: UserService) -> Generator[UserResponse, None, None]:
    user = user_service.create_user(create_user_payload())
    yield user
    user_service.delete_user(user.id)
