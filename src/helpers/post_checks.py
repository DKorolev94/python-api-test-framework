from src.models.responses.post import PostResponse


def all_posts_belong_to_user(posts: list[PostResponse], user_id: int) -> bool:
    """Возвращает true, если все посты принадлежат пользователю с указанным user_id."""
    return bool(posts) and all(p.user_id == user_id for p in posts)


def post_ids(posts: list[PostResponse]) -> set[int]:
    """Возвращает множество id всех постов."""
    return {p.id for p in posts}
