import allure
import httpx

from src.api.base_api_client import AuthenticatedAPIClient, pagination_params
from src.api.routes import UsersRoutes


class UsersAPI(AuthenticatedAPIClient):
    """HTTP клиент для работы с пользователями."""

    @allure.step("Получить список пользователей")
    def get_users(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        """Возвращает список пользователей с пагинацией."""
        return self.get(UsersRoutes.USERS, params=pagination_params(page, per_page) or None)

    @allure.step("Получить пользователя по id")
    def get_user(self, user_id: int) -> httpx.Response:
        """Возвращает одного пользователя по id."""
        return self.get(UsersRoutes.USER_BY_ID.format(user_id=user_id))

    @allure.step("Создать пользователя")
    def create_user(self, payload: dict) -> httpx.Response:
        """Создаёт нового пользователя."""
        return self.post(UsersRoutes.USERS, json=payload)

    @allure.step("Обновить пользователя")
    def update_user(self, user_id: int, payload: dict) -> httpx.Response:
        """Обновляет данные существующего пользователя."""
        return self.patch(UsersRoutes.USER_BY_ID.format(user_id=user_id), json=payload)

    @allure.step("Удалить пользователя")
    def delete_user(self, user_id: int) -> httpx.Response:
        """Удаляет пользователя по id."""
        return self.delete(UsersRoutes.USER_BY_ID.format(user_id=user_id))
