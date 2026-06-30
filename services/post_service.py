from api.posts import PostsAPI
from models.requests.post import CreatePostRequest, UpdatePostRequest
from models.responses.post import PostResponse


class PostService:
    def __init__(self, posts_api: PostsAPI):
        self.posts_api = posts_api

    def get_posts(self, page: int | None = None, per_page: int | None = None) -> list[PostResponse]:
        response = self.posts_api.get_posts(page=page, per_page=per_page)
        response.raise_for_status()
        return [PostResponse.model_validate(p) for p in response.json()]

    def get_post(self, post_id: int) -> PostResponse:
        response = self.posts_api.get_post(post_id)
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def get_user_posts(self, user_id: int) -> list[PostResponse]:
        response = self.posts_api.get_user_posts(user_id)
        response.raise_for_status()
        return [PostResponse.model_validate(p) for p in response.json()]

    def create_post(self, payload: CreatePostRequest) -> PostResponse:
        response = self.posts_api.create_post(payload.model_dump(mode="json"))
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def update_post(self, post_id: int, payload: UpdatePostRequest) -> PostResponse:
        response = self.posts_api.update_post(post_id, payload.model_dump(exclude_none=True, mode="json"))
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def delete_post(self, post_id: int) -> None:
        response = self.posts_api.delete_post(post_id)
        response.raise_for_status()
