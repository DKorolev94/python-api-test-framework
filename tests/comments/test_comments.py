from http import HTTPStatus

import allure
import pytest

from src.api.clients.comments import CommentsAPI
from src.api.services.comment_service import CommentService
from src.assertions.common_assertions import assert_equal, assert_greater, assert_in, assert_not_empty
from src.assertions.response_assertions import assert_list_schema_valid, assert_schema_valid, assert_status_code
from src.factories.comment import create_comment_payload_dict
from src.helpers.comment_checks import comment_ids
from src.models.responses.comment import CommentResponse
from src.models.responses.post import PostResponse


@allure.epic("GoRest API")
@allure.feature("Комментарии")
@allure.story("Авторизация")
@pytest.mark.contract
class TestCommentsPermissions:
    """Запросы без токена должны отклоняться."""

    @allure.title("Неуспешное создание комментария без токена")
    def test_create_comment_no_token(self, comments_api_no_auth: CommentsAPI, created_post: PostResponse):
        """Создание комментария без токена возвращает 401."""
        response = comments_api_no_auth.create_comment(create_comment_payload_dict(post_id=created_post.id))

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)


@allure.epic("GoRest API")
@allure.feature("Комментарии")
@allure.story("Валидация")
@pytest.mark.contract
class TestCommentsSchema:
    """Проверки схемы ответа и ошибок валидации."""

    @allure.title("Успешное получение списка комментариев")
    def test_get_comments_schema(self, comments_api_no_auth: CommentsAPI):
        """Список комментариев возвращается со статусом 200 и соответствует схеме."""
        response = comments_api_no_auth.get_comments()

        assert_status_code(response, HTTPStatus.OK)
        comments = assert_list_schema_valid(response, CommentResponse)
        assert_not_empty(comments, "список комментариев не пустой")

    @allure.title("Успешное получение комментария по id")
    def test_get_comment_schema(self, comments_api_no_auth: CommentsAPI, created_comment: CommentResponse):
        """Ответ на запрос комментария по id соответствует схеме и совпадает с созданным."""
        response = comments_api_no_auth.get_comment(created_comment.id)

        assert_status_code(response, HTTPStatus.OK)
        fetched = assert_schema_valid(response, CommentResponse)
        assert_equal(fetched.id, created_comment.id, "id совпадает")
        assert_equal(fetched.post_id, created_comment.post_id, "post_id совпадает")

    @allure.title("Неуспешное получение несуществующего комментария")
    def test_get_comment_not_found(self, comments_api_no_auth: CommentsAPI):
        """Запрос несуществующего комментария возвращает 404."""
        response = comments_api_no_auth.get_comment(0)

        assert_status_code(response, HTTPStatus.NOT_FOUND)

    @allure.title("Неуспешное создание комментария с неверным email")
    def test_create_comment_invalid_email(self, comments_api: CommentsAPI, created_post: PostResponse):
        """Создание комментария с неверным email возвращает 422."""
        response = comments_api.create_comment(
            create_comment_payload_dict(post_id=created_post.id, email="bad-email")
        )

        assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)


@allure.epic("GoRest API")
@allure.feature("Комментарии")
@allure.story("Создание")
@pytest.mark.integration
class TestCommentsCreate:
    """Создание комментария возвращает корректный объект."""

    @allure.title("Успешное создание комментария")
    def test_create_comment_success(self, created_comment: CommentResponse, created_post: PostResponse):
        """У созданного комментария настоящий id и он ссылается на правильный пост."""
        assert_greater(created_comment.id, 0, "id комментария больше 0")
        assert_equal(created_comment.post_id, created_post.id, "post_id комментария совпадает")

    @allure.title("Успешное отображение комментария в списке комментариев поста")
    def test_comment_in_post_comments(
        self, comment_service: CommentService, created_post: PostResponse, created_comment: CommentResponse
    ):
        """Созданный комментарий появляется среди комментариев поста."""
        post_comments = comment_service.get_post_comments(created_post.id)
        assert_in(created_comment.id, comment_ids(post_comments), "комментарий присутствует среди комментариев поста")
