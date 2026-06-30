from models.responses.post import PostResponse


def all_posts_belong_to_user(posts: list[PostResponse], user_id: int) -> bool:
    """True if all posts have the given user_id."""
    return bool(posts) and all(p.user_id == user_id for p in posts)


def post_ids(posts: list[PostResponse]) -> set[int]:
    """Returns set of all post IDs."""
    return {p.id for p in posts}
