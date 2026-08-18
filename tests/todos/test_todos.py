from http import HTTPStatus

import allure
import pytest

from src.api.clients.todos import TodosAPI
from src.api.services.todo_service import TodoService
from src.assertions.common_assertions import assert_equal, assert_greater, assert_in, assert_not_empty, assert_true
from src.assertions.response_assertions import assert_list_schema_valid, assert_schema_valid, assert_status_code
from src.factories.todo import create_todo_payload_dict, update_todo_payload
from src.helpers.todo_checks import all_todos_belong_to_user, todo_ids
from src.models.responses.todo import TodoResponse
from src.models.responses.user import UserResponse


@allure.epic("GoRest API")
@allure.feature("Задачи")
@allure.story("Авторизация")
@pytest.mark.contract
class TestTodosPermissions:
    """Запросы без токена должны отклоняться."""

    @allure.title("Неуспешное создание задачи без токена")
    def test_create_todo_no_token(self, todos_api_no_auth: TodosAPI, created_user: UserResponse):
        """Создание задачи без токена возвращает 401."""
        response = todos_api_no_auth.create_todo(create_todo_payload_dict(user_id=created_user.id))

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)


@allure.epic("GoRest API")
@allure.feature("Задачи")
@allure.story("Валидация")
@pytest.mark.contract
class TestTodosSchema:
    """Проверки схемы ответа и ошибок валидации."""

    @allure.title("Успешное получение списка задач")
    def test_get_todos_schema(self, todos_api_no_auth: TodosAPI):
        """Список задач возвращается со статусом 200 и соответствует схеме."""
        response = todos_api_no_auth.get_todos()

        assert_status_code(response, HTTPStatus.OK)
        todos = assert_list_schema_valid(response, TodoResponse)
        assert_not_empty(todos, "список задач не пустой")

    @allure.title("Успешное получение задачи по id")
    def test_get_todo_schema(self, todos_api_no_auth: TodosAPI, created_todo: TodoResponse):
        """Ответ на запрос задачи по id соответствует схеме и совпадает с созданной."""
        response = todos_api_no_auth.get_todo(created_todo.id)

        assert_status_code(response, HTTPStatus.OK)
        fetched = assert_schema_valid(response, TodoResponse)
        assert_equal(fetched.id, created_todo.id, "id совпадает")
        assert_equal(fetched.user_id, created_todo.user_id, "user_id совпадает")

    @allure.title("Неуспешное получение несуществующей задачи")
    def test_get_todo_not_found(self, todos_api_no_auth: TodosAPI):
        """Запрос несуществующей задачи возвращает 404."""
        response = todos_api_no_auth.get_todo(0)

        assert_status_code(response, HTTPStatus.NOT_FOUND)

    @allure.title("Неуспешное создание задачи без title")
    def test_create_todo_missing_title(self, todos_api: TodosAPI, created_user: UserResponse):
        """Создание задачи без обязательного поля title возвращает 422."""
        payload = create_todo_payload_dict(user_id=created_user.id)
        payload.pop("title")

        response = todos_api.create_todo(payload)

        assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)


@allure.epic("GoRest API")
@allure.feature("Задачи")
@allure.story("Создание")
@pytest.mark.integration
class TestTodosCreate:
    """Создание задачи возвращает корректный объект."""

    @allure.title("Успешное создание задачи")
    def test_create_todo_success(self, created_todo: TodoResponse, created_user: UserResponse):
        """У созданной задачи настоящий id, правильный автор и статус pending."""
        assert_greater(created_todo.id, 0, "id задачи больше 0")
        assert_equal(created_todo.user_id, created_user.id, "user_id задачи совпадает")
        assert_equal(created_todo.status, "pending", "новая задача в статусе pending")


@allure.epic("GoRest API")
@allure.feature("Задачи")
@allure.story("Обновление")
@pytest.mark.integration
class TestTodosUpdate:
    """Обновление полей существующей задачи."""

    @allure.title("Успешное обновление статуса задачи на completed")
    def test_update_todo_status(self, todo_service: TodoService, created_todo: TodoResponse):
        """После обновления статуса задача становится completed."""
        updated = todo_service.update_todo(created_todo.id, update_todo_payload(status="completed"))

        assert_equal(updated.status, "completed", "статус обновлён на completed")


@allure.epic("GoRest API")
@allure.feature("Задачи")
@allure.story("Задачи пользователя")
@pytest.mark.integration
class TestTodosByUser:
    """Фильтрация задач по пользователю."""

    @allure.title("Успешное получение задач конкретного пользователя")
    def test_user_todos_belong_to_user(
        self, todo_service: TodoService, created_user: UserResponse, created_todo: TodoResponse
    ):
        """Все задачи, возвращённые для пользователя, принадлежат именно ему."""
        todos = todo_service.get_user_todos(created_user.id)

        assert_true(all_todos_belong_to_user(todos, created_user.id), "все задачи принадлежат пользователю")
        assert_in(created_todo.id, todo_ids(todos), "созданная задача присутствует в списке")
