import allure
import httpx

from src.api.base_api_client import AuthenticatedAPIClient, pagination_params
from src.api.routes import PostsRoutes


class PostsAPI(AuthenticatedAPIClient):
    """HTTP клиент для работы с постами."""

    @allure.step("Получить список постов")
    def get_posts(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        """Возвращает список постов с пагинацией."""
        return self.get(PostsRoutes.POSTS, params=pagination_params(page, per_page) or None)

    @allure.step("Получить пост по id")
    def get_post(self, post_id: int) -> httpx.Response:
        """Возвращает один пост по id."""
        return self.get(PostsRoutes.POST_BY_ID.format(post_id=post_id))

    @allure.step("Получить посты пользователя")
    def get_user_posts(self, user_id: int) -> httpx.Response:
        """Возвращает все посты конкретного пользователя."""
        return self.get(PostsRoutes.USER_POSTS.format(user_id=user_id))

    @allure.step("Создать пост")
    def create_post(self, payload: dict) -> httpx.Response:
        """Создаёт новый пост."""
        return self.post(PostsRoutes.POSTS, json=payload)

    @allure.step("Обновить пост")
    def update_post(self, post_id: int, payload: dict) -> httpx.Response:
        """Обновляет данные существующего поста."""
        return self.patch(PostsRoutes.POST_BY_ID.format(post_id=post_id), json=payload)

    @allure.step("Удалить пост")
    def delete_post(self, post_id: int) -> httpx.Response:
        """Удаляет пост по id."""
        return self.delete(PostsRoutes.POST_BY_ID.format(post_id=post_id))
