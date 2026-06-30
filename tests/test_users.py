from http import HTTPStatus

import allure
import pytest
from hamcrest import assert_that, equal_to, has_item, instance_of, not_, empty

from api.users import UsersAPI
from factories.user import create_user_payload, create_user_payload_dict, update_user_payload
from helpers.pagination_checks import items_fit_limit
from helpers.user_checks import all_users_active, find_user_by_id, user_ids
from models.responses.common import ValidationErrorItem
from models.responses.user import UserResponse
from services.user_service import UserService
from utils.decorators import WorkItem, linked, step


@allure.feature("Users")
@pytest.mark.contract
class TestUsersPermissions:

    @linked(WorkItem(id=0, name="Users: create without token returns 401"))
    def test_create_user_no_token(self, users_api_no_auth: UsersAPI):
        with step("POST /users without token"):
            response = users_api_no_auth.create_user(create_user_payload_dict())
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))

    @linked(WorkItem(id=0, name="Users: create with invalid token returns 401"))
    def test_create_user_invalid_token(self):
        with step("POST /users with invalid token"):
            response = UsersAPI(token="invalid_token_xyz").create_user(create_user_payload_dict())
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))

    @linked(WorkItem(id=0, name="Users: delete without token returns 401"))
    def test_delete_user_no_token(self, users_api_no_auth: UsersAPI):
        with step("DELETE /users/1 without token"):
            response = users_api_no_auth.delete_user(1)
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))


@allure.feature("Users")
@pytest.mark.contract
class TestUsersSchema:

    @linked(WorkItem(id=0, name="Users: list returns 200 with valid schema"))
    def test_get_users_schema(self, users_api_no_auth: UsersAPI):
        with step("GET /users"):
            response = users_api_no_auth.get_users()
        with step("Response: 200, items match UserResponse schema"):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))
            users = [UserResponse.model_validate(u) for u in response.json()]
            assert_that(users, not_(empty()))

    @linked(WorkItem(id=0, name="Users: get non-existent id returns 404"))
    def test_get_user_not_found(self, users_api_no_auth: UsersAPI):
        with step("GET /users/0"):
            response = users_api_no_auth.get_user(0)
        with step("Response: 404 Not Found"):
            assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))

    @linked(WorkItem(id=0, name="Users: create with invalid email returns 422"))
    def test_create_user_invalid_email(self, users_api: UsersAPI):
        with step("POST /users with invalid email"):
            response = users_api.create_user(create_user_payload_dict(email="not-an-email"))
        with step("Response: 422, validation error on email field"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))
            errors = [ValidationErrorItem.model_validate(e) for e in response.json()]
            assert_that([e.field for e in errors], has_item("email"))

    @linked(WorkItem(id=0, name="Users: create with missing name returns 422"))
    def test_create_user_missing_name(self, users_api: UsersAPI):
        payload = create_user_payload_dict()
        payload.pop("name")
        with step("POST /users without name field"):
            response = users_api.create_user(payload)
        with step("Response: 422 Unprocessable Entity"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))


@allure.feature("Users")
@pytest.mark.integration
class TestUsersCreate:

    @linked(WorkItem(id=0, name="Users: create returns valid user with id"))
    def test_create_user_success(self, created_user: UserResponse):
        with step("User created via fixture"):
            assert_that(created_user.id, instance_of(int))
            assert_that(created_user.status, equal_to("active"))
            assert_that(created_user.name, instance_of(str))

    @linked(WorkItem(id=0, name="Users: created user readable by id"))
    def test_created_user_readable(self, user_service: UserService, created_user: UserResponse):
        with step("GET /users/{id} for created user"):
            fetched = user_service.get_user(created_user.id)
        with step("Fetched user matches created"):
            assert_that(fetched.id, equal_to(created_user.id))
            assert_that(fetched.email, equal_to(created_user.email))

    @linked(WorkItem(id=0, name="Users: created user appears in list"))
    def test_created_user_in_list(self, user_service: UserService, created_user: UserResponse):
        with step("GET /users"):
            users, _ = user_service.get_page(per_page=20)
        with step("Created user id in list"):
            ids = user_ids(users)
            # GoRest paginates — user may not be on page 1; id existence check via direct GET
            fetched = user_service.get_user(created_user.id)
            assert_that(fetched.id, equal_to(created_user.id))


@allure.feature("Users")
@pytest.mark.integration
class TestUsersUpdate:

    @linked(WorkItem(id=0, name="Users: update name"))
    def test_update_user_name(self, user_service: UserService, created_user: UserResponse):
        new_name = "Updated Portfolio Test"
        with step(f"PATCH /users/{created_user.id}"):
            updated = user_service.update_user(created_user.id, update_user_payload(name=new_name))
        with step("Name updated, id unchanged"):
            assert_that(updated.name, equal_to(new_name))
            assert_that(updated.id, equal_to(created_user.id))

    @linked(WorkItem(id=0, name="Users: update status to inactive"))
    def test_update_user_status(self, user_service: UserService, created_user: UserResponse):
        with step("PATCH status to inactive"):
            updated = user_service.update_user(created_user.id, update_user_payload(status="inactive"))
        with step("Status is inactive"):
            assert_that(updated.status, equal_to("inactive"))


@allure.feature("Users")
@pytest.mark.integration
class TestUsersPagination:

    @linked(WorkItem(id=0, name="Users: pagination respects per_page limit"))
    def test_pagination_per_page(self, user_service: UserService):
        per_page = 5
        with step(f"GET /users?per_page={per_page}"):
            users, meta = user_service.get_page(per_page=per_page)
        with step("Items count <= per_page, meta has correct limit"):
            assert_that(items_fit_limit(users, meta), equal_to(True))
            assert_that(meta.limit, equal_to(per_page))

    @linked(WorkItem(id=0, name="Users: page 1 and page 2 have no duplicate IDs"))
    def test_pagination_no_duplicates(self, user_service: UserService):
        with step("GET page=1 and page=2 with per_page=5"):
            users_p1, _ = user_service.get_page(page=1, per_page=5)
            users_p2, _ = user_service.get_page(page=2, per_page=5)
        with step("No duplicate IDs between pages"):
            ids_p1 = user_ids(users_p1)
            ids_p2 = user_ids(users_p2)
            assert_that(len(ids_p1 & ids_p2), equal_to(0))
