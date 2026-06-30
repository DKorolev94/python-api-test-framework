from models.responses.user import UserResponse


def all_users_active(users: list[UserResponse]) -> bool:
    """True if all users have status 'active'."""
    return bool(users) and all(u.status == "active" for u in users)


def user_ids(users: list[UserResponse]) -> set[int]:
    """Returns set of all user IDs."""
    return {u.id for u in users}


def find_user_by_id(users: list[UserResponse], user_id: int) -> UserResponse | None:
    """Returns first user with given id, or None."""
    return next((u for u in users if u.id == user_id), None)
