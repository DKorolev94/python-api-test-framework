from src.api.clients.todos import TodosAPI
from src.models.requests.todo import CreateTodoRequest, UpdateTodoRequest
from src.models.responses.todo import TodoResponse


class TodoService:
    """Разбирает ответы todo API в модели TodoResponse."""

    def __init__(self, todos_api: TodosAPI):
        self.todos_api = todos_api

    def get_todos(self, page: int | None = None, per_page: int | None = None) -> list[TodoResponse]:
        """Возвращает список задач постранично и валидирует их в модели TodoResponse."""
        response = self.todos_api.get_todos(page=page, per_page=per_page)
        response.raise_for_status()
        return [TodoResponse.model_validate(t) for t in response.json()]

    def get_todo(self, todo_id: int) -> TodoResponse:
        """Возвращает задачу по id и валидирует её в модель TodoResponse."""
        response = self.todos_api.get_todo(todo_id)
        response.raise_for_status()
        return TodoResponse.model_validate(response.json())

    def get_user_todos(self, user_id: int) -> list[TodoResponse]:
        """Возвращает все задачи пользователя и валидирует их в модели TodoResponse."""
        response = self.todos_api.get_user_todos(user_id)
        response.raise_for_status()
        return [TodoResponse.model_validate(t) for t in response.json()]

    def create_todo(self, payload: CreateTodoRequest) -> TodoResponse:
        """Создаёт задачу и валидирует ответ в модель TodoResponse."""
        response = self.todos_api.create_todo(payload.model_dump(mode="json"))
        response.raise_for_status()
        return TodoResponse.model_validate(response.json())

    def update_todo(self, todo_id: int, payload: UpdateTodoRequest) -> TodoResponse:
        """Обновляет задачу и валидирует ответ в модель TodoResponse."""
        response = self.todos_api.update_todo(todo_id, payload.model_dump(exclude_none=True, mode="json"))
        response.raise_for_status()
        return TodoResponse.model_validate(response.json())

    def delete_todo(self, todo_id: int) -> None:
        """Удаляет задачу по id."""
        response = self.todos_api.delete_todo(todo_id)
        response.raise_for_status()
