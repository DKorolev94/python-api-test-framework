from src.api.clients.posts import PostsAPI
from src.models.requests.post import CreatePostRequest, UpdatePostRequest
from src.models.responses.post import PostResponse


class PostService:
    """Разбирает ответы post API в модели PostResponse."""

    def __init__(self, posts_api: PostsAPI):
        self.posts_api = posts_api

    def get_posts(self, page: int | None = None, per_page: int | None = None) -> list[PostResponse]:
        """Возвращает список постов постранично и валидирует их в модели PostResponse."""
        response = self.posts_api.get_posts(page=page, per_page=per_page)
        response.raise_for_status()
        return [PostResponse.model_validate(p) for p in response.json()]

    def get_post(self, post_id: int) -> PostResponse:
        """Возвращает пост по id и валидирует его в модель PostResponse."""
        response = self.posts_api.get_post(post_id)
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def get_user_posts(self, user_id: int) -> list[PostResponse]:
        """Возвращает все посты пользователя и валидирует их в модели PostResponse."""
        response = self.posts_api.get_user_posts(user_id)
        response.raise_for_status()
        return [PostResponse.model_validate(p) for p in response.json()]

    def create_post(self, payload: CreatePostRequest) -> PostResponse:
        """Создаёт пост и валидирует ответ в модель PostResponse."""
        response = self.posts_api.create_post(payload.model_dump(mode="json"))
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def update_post(self, post_id: int, payload: UpdatePostRequest) -> PostResponse:
        """Обновляет пост и валидирует ответ в модель PostResponse."""
        response = self.posts_api.update_post(post_id, payload.model_dump(exclude_none=True, mode="json"))
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def delete_post(self, post_id: int) -> None:
        """Удаляет пост по id."""
        response = self.posts_api.delete_post(post_id)
        response.raise_for_status()
