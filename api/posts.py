import httpx

from api.core.base_api_client import BaseAPIClient
from config.settings import settings

POSTS = "posts"
POST_BY_ID = "posts/{post_id}"
USER_POSTS = "users/{user_id}/posts"


class PostsAPI(BaseAPIClient):
    def __init__(self, token: str | None = None, base_url: str | None = None, **kwargs):
        super().__init__(base_url=base_url or settings.BASE_URL, **kwargs)
        if token:
            self.client.headers["Authorization"] = f"Bearer {token}"

    def get_posts(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self.get(POSTS, params=params or None)

    def get_post(self, post_id: int) -> httpx.Response:
        return self.get(POST_BY_ID.format(post_id=post_id))

    def get_user_posts(self, user_id: int) -> httpx.Response:
        return self.get(USER_POSTS.format(user_id=user_id))

    def create_post(self, payload: dict) -> httpx.Response:
        return self.post(POSTS, json=payload)

    def update_post(self, post_id: int, payload: dict) -> httpx.Response:
        return self.patch(POST_BY_ID.format(post_id=post_id), json=payload)

    def delete_post(self, post_id: int) -> httpx.Response:
        return self.delete(POST_BY_ID.format(post_id=post_id))
