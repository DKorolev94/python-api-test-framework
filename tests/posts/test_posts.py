from http import HTTPStatus

import allure
import pytest

from src.api.clients.posts import PostsAPI
from src.api.services.post_service import PostService
from src.assertions.common_assertions import assert_equal, assert_greater, assert_in, assert_not_empty, assert_true
from src.assertions.response_assertions import assert_list_schema_valid, assert_schema_valid, assert_status_code
from src.factories.post import create_post_payload_dict, update_post_payload
from src.helpers.post_checks import all_posts_belong_to_user, post_ids
from src.models.responses.post import PostResponse
from src.models.responses.user import UserResponse


@allure.epic("GoRest API")
@allure.feature("Посты")
@allure.story("Авторизация")
@pytest.mark.contract
class TestPostsPermissions:
    """Запросы без токена должны отклоняться."""

    @allure.title("Неуспешное создание поста без токена")
    def test_create_post_no_token(self, posts_api_no_auth: PostsAPI, created_user: UserResponse):
        """Создание поста без токена возвращает 401."""
        response = posts_api_no_auth.create_post(create_post_payload_dict(user_id=created_user.id))

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

    @allure.title("Неуспешное удаление поста без токена")
    def test_delete_post_no_token(self, posts_api_no_auth: PostsAPI, created_post: PostResponse):
        """Удаление поста без токена возвращает 401."""
        response = posts_api_no_auth.delete_post(created_post.id)

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)


@allure.epic("GoRest API")
@allure.feature("Посты")
@allure.story("Валидация")
@pytest.mark.contract
class TestPostsSchema:
    """Проверки схемы ответа и ошибок валидации."""

    @allure.title("Успешное получение списка постов")
    def test_get_posts_schema(self, posts_api_no_auth: PostsAPI):
        """Список постов возвращается со статусом 200 и соответствует схеме."""
        response = posts_api_no_auth.get_posts()

        assert_status_code(response, HTTPStatus.OK)
        posts = assert_list_schema_valid(response, PostResponse)
        assert_not_empty(posts, "список постов не пустой")

    @allure.title("Успешное получение поста по id")
    def test_get_post_schema(self, posts_api_no_auth: PostsAPI, created_post: PostResponse):
        """Ответ на запрос поста по id соответствует схеме и совпадает с созданным."""
        response = posts_api_no_auth.get_post(created_post.id)

        assert_status_code(response, HTTPStatus.OK)
        fetched = assert_schema_valid(response, PostResponse)
        assert_equal(fetched.id, created_post.id, "id совпадает")
        assert_equal(fetched.title, created_post.title, "title совпадает")

    @allure.title("Неуспешное получение несуществующего поста")
    def test_get_post_not_found(self, posts_api_no_auth: PostsAPI):
        """Запрос несуществующего поста возвращает 404."""
        response = posts_api_no_auth.get_post(0)

        assert_status_code(response, HTTPStatus.NOT_FOUND)

    @allure.title("Неуспешное создание поста без title")
    def test_create_post_missing_title(self, posts_api: PostsAPI, created_user: UserResponse):
        """Создание поста без обязательного поля title возвращает 422."""
        payload = create_post_payload_dict(user_id=created_user.id)
        payload.pop("title")

        response = posts_api.create_post(payload)

        assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)


@allure.epic("GoRest API")
@allure.feature("Посты")
@allure.story("Создание")
@pytest.mark.integration
class TestPostsCreate:
    """Создание поста возвращает корректный объект."""

    @allure.title("Успешное создание поста")
    def test_create_post_success(self, created_post: PostResponse, created_user: UserResponse):
        """У созданного поста настоящий id и правильный автор."""
        assert_greater(created_post.id, 0, "id поста больше 0")
        assert_equal(created_post.user_id, created_user.id, "user_id поста совпадает с автором")


@allure.epic("GoRest API")
@allure.feature("Посты")
@allure.story("Обновление")
@pytest.mark.integration
class TestPostsUpdate:
    """Обновление полей существующего поста."""

    @allure.title("Успешное обновление заголовка поста")
    def test_update_post_title(self, post_service: PostService, created_post: PostResponse):
        """После обновления заголовка пост сохраняет новое значение."""
        new_title = "Updated Post Title"

        updated = post_service.update_post(created_post.id, update_post_payload(title=new_title))

        assert_equal(updated.title, new_title, "заголовок обновлён")
        assert_equal(updated.id, created_post.id, "id не изменился")


@allure.epic("GoRest API")
@allure.feature("Посты")
@allure.story("Посты пользователя")
@pytest.mark.integration
class TestPostsByUser:
    """Фильтрация постов по автору."""

    @allure.title("Успешное получение постов конкретного пользователя")
    def test_user_posts_belong_to_user(
        self, post_service: PostService, created_user: UserResponse, created_post: PostResponse
    ):
        """Все посты, возвращённые для пользователя, принадлежат именно ему."""
        posts = post_service.get_user_posts(created_user.id)

        assert_true(all_posts_belong_to_user(posts, created_user.id), "все посты принадлежат пользователю")
        assert_in(created_post.id, post_ids(posts), "созданный пост присутствует в списке")
