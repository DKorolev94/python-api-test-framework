import allure
import httpx

from src.api.base_api_client import AuthenticatedAPIClient, pagination_params
from src.api.routes import TodosRoutes


class TodosAPI(AuthenticatedAPIClient):
    """HTTP клиент для работы с задачами."""

    @allure.step("Получить список задач")
    def get_todos(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        """Возвращает список задач с пагинацией."""
        return self.get(TodosRoutes.TODOS, params=pagination_params(page, per_page) or None)

    @allure.step("Получить задачу по id")
    def get_todo(self, todo_id: int) -> httpx.Response:
        """Возвращает одну задачу по id."""
        return self.get(TodosRoutes.TODO_BY_ID.format(todo_id=todo_id))

    @allure.step("Получить задачи пользователя")
    def get_user_todos(self, user_id: int) -> httpx.Response:
        """Возвращает все задачи конкретного пользователя."""
        return self.get(TodosRoutes.USER_TODOS.format(user_id=user_id))

    @allure.step("Создать задачу")
    def create_todo(self, payload: dict) -> httpx.Response:
        """Создаёт новую задачу."""
        return self.post(TodosRoutes.TODOS, json=payload)

    @allure.step("Обновить задачу")
    def update_todo(self, todo_id: int, payload: dict) -> httpx.Response:
        """Обновляет данные существующей задачи."""
        return self.patch(TodosRoutes.TODO_BY_ID.format(todo_id=todo_id), json=payload)

    @allure.step("Удалить задачу")
    def delete_todo(self, todo_id: int) -> httpx.Response:
        """Удаляет задачу по id."""
        return self.delete(TodosRoutes.TODO_BY_ID.format(todo_id=todo_id))
