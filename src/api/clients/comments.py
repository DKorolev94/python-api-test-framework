import allure
import httpx

from src.api.base_api_client import AuthenticatedAPIClient, pagination_params
from src.api.routes import CommentsRoutes


class CommentsAPI(AuthenticatedAPIClient):
    """HTTP клиент для работы с комментариями."""

    @allure.step("Получить список комментариев")
    def get_comments(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        """Возвращает список комментариев с пагинацией."""
        return self.get(CommentsRoutes.COMMENTS, params=pagination_params(page, per_page) or None)

    @allure.step("Получить комментарии поста")
    def get_post_comments(self, post_id: int) -> httpx.Response:
        """Возвращает все комментарии конкретного поста."""
        return self.get(CommentsRoutes.POST_COMMENTS.format(post_id=post_id))

    @allure.step("Получить комментарий по id")
    def get_comment(self, comment_id: int) -> httpx.Response:
        """Возвращает один комментарий по id."""
        return self.get(CommentsRoutes.COMMENT_BY_ID.format(comment_id=comment_id))

    @allure.step("Создать комментарий")
    def create_comment(self, payload: dict) -> httpx.Response:
        """Создаёт новый комментарий."""
        return self.post(CommentsRoutes.COMMENTS, json=payload)

    @allure.step("Удалить комментарий")
    def delete_comment(self, comment_id: int) -> httpx.Response:
        """Удаляет комментарий по id."""
        return self.delete(CommentsRoutes.COMMENT_BY_ID.format(comment_id=comment_id))
