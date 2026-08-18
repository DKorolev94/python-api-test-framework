from src.models.responses.todo import TodoResponse


def all_todos_belong_to_user(todos: list[TodoResponse], user_id: int) -> bool:
    """Возвращает true, если все задачи принадлежат пользователю с указанным user_id."""
    return bool(todos) and all(t.user_id == user_id for t in todos)


def todo_ids(todos: list[TodoResponse]) -> set[int]:
    """Возвращает множество id всех задач."""
    return {t.id for t in todos}
