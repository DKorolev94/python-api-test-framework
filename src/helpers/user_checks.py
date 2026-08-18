from src.models.responses.user import UserResponse


def user_ids(users: list[UserResponse]) -> set[int]:
    """Возвращает множество id всех пользователей."""
    return {u.id for u in users}
