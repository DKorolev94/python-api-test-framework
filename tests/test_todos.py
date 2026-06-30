from http import HTTPStatus

import allure
import pytest
from hamcrest import assert_that, equal_to, has_item, instance_of, not_, empty

from api.todos import TodosAPI
from factories.todo import create_todo_payload, create_todo_payload_dict, update_todo_payload
from models.responses.todo import TodoResponse
from models.responses.user import UserResponse
from services.todo_service import TodoService
from utils.decorators import WorkItem, linked, step


@allure.feature("Todos")
@pytest.mark.contract
class TestTodosPermissions:

    @linked(WorkItem(id=0, name="Todos: create without token returns 401"))
    def test_create_todo_no_token(self, todos_api_no_auth: TodosAPI, created_user: UserResponse):
        with step("POST /todos without token"):
            response = todos_api_no_auth.create_todo(
                create_todo_payload_dict(user_id=created_user.id)
            )
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))


@allure.feature("Todos")
@pytest.mark.contract
class TestTodosSchema:

    @linked(WorkItem(id=0, name="Todos: list returns 200 with valid schema"))
    def test_get_todos_schema(self, todos_api_no_auth: TodosAPI):
        with step("GET /todos"):
            response = todos_api_no_auth.get_todos()
        with step("Response: 200, items match TodoResponse schema"):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))
            todos = [TodoResponse.model_validate(t) for t in response.json()]
            assert_that(todos, not_(empty()))

    @linked(WorkItem(id=0, name="Todos: get non-existent returns 404"))
    def test_get_todo_not_found(self, todos_api_no_auth: TodosAPI):
        with step("GET /todos/0"):
            response = todos_api_no_auth.get_todo(0)
        with step("Response: 404 Not Found"):
            assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))

    @linked(WorkItem(id=0, name="Todos: create with missing title returns 422"))
    def test_create_todo_missing_title(self, todos_api: TodosAPI, created_user: UserResponse):
        payload = create_todo_payload_dict(user_id=created_user.id)
        payload.pop("title")
        with step("POST /todos without title"):
            response = todos_api.create_todo(payload)
        with step("Response: 422 Unprocessable Entity"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))


@allure.feature("Todos")
@pytest.mark.integration
class TestTodosCreate:

    @linked(WorkItem(id=0, name="Todos: create returns valid todo"))
    def test_create_todo_success(
        self, todo_service: TodoService, created_user: UserResponse
    ):
        payload = create_todo_payload(user_id=created_user.id)
        with step("POST /todos"):
            todo = todo_service.create_todo(payload)
        with step("Todo created with correct user_id and pending status"):
            assert_that(todo.id, instance_of(int))
            assert_that(todo.user_id, equal_to(created_user.id))
            assert_that(todo.status, equal_to("pending"))
        with step("Cleanup"):
            todo_service.delete_todo(todo.id)


@allure.feature("Todos")
@pytest.mark.integration
class TestTodosUpdate:

    @linked(WorkItem(id=0, name="Todos: update status to completed"))
    def test_update_todo_status(
        self, todo_service: TodoService, created_user: UserResponse
    ):
        todo = todo_service.create_todo(create_todo_payload(user_id=created_user.id))
        try:
            with step("PATCH /todos/{id} status to completed"):
                updated = todo_service.update_todo(todo.id, update_todo_payload(status="completed"))
            with step("Status is completed"):
                assert_that(updated.status, equal_to("completed"))
        finally:
            todo_service.delete_todo(todo.id)


@allure.feature("Todos")
@pytest.mark.integration
class TestTodosByUser:

    @linked(WorkItem(id=0, name="Todos: user todos all belong to user"))
    def test_user_todos_belong_to_user(
        self, todo_service: TodoService, created_user: UserResponse
    ):
        todo = todo_service.create_todo(create_todo_payload(user_id=created_user.id))
        try:
            with step("GET /users/{id}/todos"):
                todos = todo_service.get_user_todos(created_user.id)
            with step("All todos have correct user_id"):
                assert_that(all(t.user_id == created_user.id for t in todos), equal_to(True))
                assert_that({t.id for t in todos}, has_item(todo.id))
        finally:
            todo_service.delete_todo(todo.id)
