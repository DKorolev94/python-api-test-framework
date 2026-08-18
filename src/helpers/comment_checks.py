from src.models.responses.comment import CommentResponse


def comment_ids(comments: list[CommentResponse]) -> set[int]:
    """Возвращает множество id всех комментариев."""
    return {c.id for c in comments}
