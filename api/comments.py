import httpx

from api.core.base_api_client import BaseAPIClient
from config.settings import settings

COMMENTS = "comments"
COMMENT_BY_ID = "comments/{comment_id}"
POST_COMMENTS = "posts/{post_id}/comments"


class CommentsAPI(BaseAPIClient):
    def __init__(self, token: str | None = None, base_url: str | None = None, **kwargs):
        super().__init__(base_url=base_url or settings.BASE_URL, **kwargs)
        if token:
            self.client.headers["Authorization"] = f"Bearer {token}"

    def get_comments(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self.get(COMMENTS, params=params or None)

    def get_post_comments(self, post_id: int) -> httpx.Response:
        return self.get(POST_COMMENTS.format(post_id=post_id))

    def get_comment(self, comment_id: int) -> httpx.Response:
        return self.get(COMMENT_BY_ID.format(comment_id=comment_id))

    def create_comment(self, payload: dict) -> httpx.Response:
        return self.post(COMMENTS, json=payload)

    def delete_comment(self, comment_id: int) -> httpx.Response:
        return self.delete(COMMENT_BY_ID.format(comment_id=comment_id))
