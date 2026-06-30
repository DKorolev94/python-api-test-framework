import httpx

from api.core.base_api_client import BaseAPIClient
from config.settings import settings

TODOS = "todos"
TODO_BY_ID = "todos/{todo_id}"
USER_TODOS = "users/{user_id}/todos"


class TodosAPI(BaseAPIClient):
    def __init__(self, token: str | None = None, base_url: str | None = None, **kwargs):
        super().__init__(base_url=base_url or settings.BASE_URL, **kwargs)
        if token:
            self.client.headers["Authorization"] = f"Bearer {token}"

    def get_todos(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self.get(TODOS, params=params or None)

    def get_todo(self, todo_id: int) -> httpx.Response:
        return self.get(TODO_BY_ID.format(todo_id=todo_id))

    def get_user_todos(self, user_id: int) -> httpx.Response:
        return self.get(USER_TODOS.format(user_id=user_id))

    def create_todo(self, payload: dict) -> httpx.Response:
        return self.post(TODOS, json=payload)

    def update_todo(self, todo_id: int, payload: dict) -> httpx.Response:
        return self.patch(TODO_BY_ID.format(todo_id=todo_id), json=payload)

    def delete_todo(self, todo_id: int) -> httpx.Response:
        return self.delete(TODO_BY_ID.format(todo_id=todo_id))
