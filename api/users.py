import httpx

from api.core.base_api_client import BaseAPIClient
from config.settings import settings

USERS = "users"
USER_BY_ID = "users/{user_id}"

class UsersAPI(BaseAPIClient):
    def __init__(self, token: str | None = None, base_url: str | None = None, **kwargs):
        super().__init__(base_url=base_url or settings.BASE_URL, **kwargs)
        if token:
            self.client.headers["Authorization"] = f"Bearer {token}"

    def get_users(self, page: int | None = None, per_page: int | None = None) -> httpx.Response:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self.get(USERS, params=params or None)

    def get_user(self, user_id: int) -> httpx.Response:
        return self.get(USER_BY_ID.format(user_id=user_id))

    def create_user(self, payload: dict) -> httpx.Response:
        return self.post(USERS, json=payload)

    def update_user(self, user_id: int, payload: dict) -> httpx.Response:
        return self.patch(USER_BY_ID.format(user_id=user_id), json=payload)

    def delete_user(self, user_id: int) -> httpx.Response:
        return self.delete(USER_BY_ID.format(user_id=user_id))
