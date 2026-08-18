"""Константы роутов для API клиентов."""


class UsersRoutes:
    """Роуты ресурса пользователей."""

    USERS = "users"
    USER_BY_ID = "users/{user_id}"


class PostsRoutes:
    """Роуты ресурса постов."""

    POSTS = "posts"
    POST_BY_ID = "posts/{post_id}"
    USER_POSTS = "users/{user_id}/posts"


class CommentsRoutes:
    """Роуты ресурса комментариев."""

    COMMENTS = "comments"
    COMMENT_BY_ID = "comments/{comment_id}"
    POST_COMMENTS = "posts/{post_id}/comments"


class TodosRoutes:
    """Роуты ресурса задач."""

    TODOS = "todos"
    TODO_BY_ID = "todos/{todo_id}"
    USER_TODOS = "users/{user_id}/todos"
