from http import HTTPStatus

import allure
import pytest

from src.api.clients.users import UsersAPI
from src.api.services.user_service import UserService
from src.assertions.common_assertions import assert_equal, assert_greater, assert_in, assert_not_empty, assert_true
from src.assertions.response_assertions import assert_list_schema_valid, assert_schema_valid, assert_status_code
from src.factories.user import create_user_payload_dict, update_user_payload
from src.helpers.pagination_checks import items_fit_limit
from src.helpers.user_checks import user_ids
from src.models.responses.common import ValidationErrorItem
from src.models.responses.user import UserResponse


@allure.epic("GoRest API")
@allure.feature("Пользователи")
@allure.story("Авторизация")
@pytest.mark.contract
class TestUsersPermissions:
    """Запросы без токена или с неправильным токеном должны отклоняться."""

    @allure.title("Неуспешное создание пользователя без токена")
    def test_create_user_no_token(self, users_api_no_auth: UsersAPI):
        """Создание пользователя без токена возвращает 401."""
        response = users_api_no_auth.create_user(create_user_payload_dict())

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

    @allure.title("Неуспешное создание пользователя с неверным токеном")
    def test_create_user_invalid_token(self):
        """Создание пользователя с неверным токеном возвращает 401."""
        with UsersAPI(token="invalid_token_xyz") as api:
            response = api.create_user(create_user_payload_dict())

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

    @allure.title("Неуспешное удаление пользователя без токена")
    def test_delete_user_no_token(self, users_api_no_auth: UsersAPI):
        """Удаление пользователя без токена возвращает 401."""
        response = users_api_no_auth.delete_user(1)

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)


@allure.epic("GoRest API")
@allure.feature("Пользователи")
@allure.story("Валидация")
@pytest.mark.contract
class TestUsersSchema:
    """Проверки схемы ответа и ошибок валидации."""

    @allure.title("Успешное получение списка пользователей")
    def test_get_users_schema(self, users_api_no_auth: UsersAPI):
        """Список пользователей возвращается со статусом 200 и соответствует схеме."""
        response = users_api_no_auth.get_users()

        assert_status_code(response, HTTPStatus.OK)
        users = assert_list_schema_valid(response, UserResponse)
        assert_not_empty(users, "список пользователей не пустой")

    @allure.title("Успешное получение пользователя по id")
    def test_get_user_schema(self, users_api_no_auth: UsersAPI, created_user: UserResponse):
        """Ответ на запрос пользователя по id соответствует схеме и совпадает с созданным."""
        response = users_api_no_auth.get_user(created_user.id)

        assert_status_code(response, HTTPStatus.OK)
        fetched = assert_schema_valid(response, UserResponse)
        assert_equal(fetched.id, created_user.id, "id совпадает")
        assert_equal(fetched.email, created_user.email, "email совпадает")

    @allure.title("Неуспешное получение несуществующего пользователя")
    def test_get_user_not_found(self, users_api_no_auth: UsersAPI):
        """Запрос несуществующего пользователя возвращает 404."""
        response = users_api_no_auth.get_user(0)

        assert_status_code(response, HTTPStatus.NOT_FOUND)

    @allure.title("Неуспешное создание пользователя с неверным email")
    def test_create_user_invalid_email(self, users_api: UsersAPI):
        """Создание пользователя с неверным email возвращает 422."""
        response = users_api.create_user(create_user_payload_dict(email="not-an-email"))

        assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)
        errors = assert_list_schema_valid(response, ValidationErrorItem)
        assert_in("email", [e.field for e in errors], "поле email присутствует в ошибках валидации")

    @allure.title("Неуспешное создание пользователя без поля name")
    def test_create_user_missing_name(self, users_api: UsersAPI):
        """Создание пользователя без обязательного поля name возвращает 422."""
        payload = create_user_payload_dict()
        payload.pop("name")

        response = users_api.create_user(payload)

        assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)


@allure.epic("GoRest API")
@allure.feature("Пользователи")
@allure.story("Создание")
@pytest.mark.integration
class TestUsersCreate:
    """Создание пользователя возвращает корректный объект."""

    @allure.title("Успешное создание пользователя")
    def test_create_user_success(self, created_user: UserResponse):
        """У созданного пользователя настоящий id и статус active по умолчанию."""
        assert_equal(created_user.status, "active", "статус созданного пользователя равен active")
        assert_greater(created_user.id, 0, "id пользователя больше 0")


@allure.epic("GoRest API")
@allure.feature("Пользователи")
@allure.story("Обновление")
@pytest.mark.integration
class TestUsersUpdate:
    """Обновление полей существующего пользователя."""

    @allure.title("Успешное обновление имени пользователя")
    def test_update_user_name(self, user_service: UserService, created_user: UserResponse):
        """После обновления имени пользователь сохраняет новое значение."""
        new_name = "Updated Portfolio Test"

        updated = user_service.update_user(created_user.id, update_user_payload(name=new_name))

        assert_equal(updated.name, new_name, "имя обновлено")
        assert_equal(updated.id, created_user.id, "id не изменился")

    @allure.title("Успешное обновление статуса пользователя на inactive")
    def test_update_user_status(self, user_service: UserService, created_user: UserResponse):
        """После обновления статуса пользователь становится inactive."""
        updated = user_service.update_user(created_user.id, update_user_payload(status="inactive"))

        assert_equal(updated.status, "inactive", "статус обновлён")


@allure.epic("GoRest API")
@allure.feature("Пользователи")
@allure.story("Пагинация")
@pytest.mark.integration
class TestUsersPagination:
    """Пагинация списка пользователей работает предсказуемо."""

    @allure.title("Успешная пагинация с ограничением per_page")
    def test_pagination_per_page(self, user_service: UserService):
        """Количество элементов на странице не превышает per_page."""
        per_page = 5

        users, meta = user_service.get_page(per_page=per_page)

        assert_true(items_fit_limit(users, meta), "количество элементов не превышает limit")
        assert_equal(meta.limit, per_page, "limit в meta совпадает с per_page")

    @allure.title("Успешная пагинация без повторов между страницами")
    def test_pagination_no_duplicates(self, user_service: UserService):
        """Страницы 1 и 2 не содержат одинаковых id."""
        with allure.step("Получить страницу 1 и страницу 2 с per_page=5"):
            users_p1, _ = user_service.get_page(page=1, per_page=5)
            users_p2, _ = user_service.get_page(page=2, per_page=5)

        ids_p1 = user_ids(users_p1)
        ids_p2 = user_ids(users_p2)
        assert_equal(len(ids_p1 & ids_p2), 0, "пересечение id между страницами пустое")
