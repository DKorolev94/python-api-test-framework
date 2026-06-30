---
paths:
  - "api/**/*.py"
---

# API Layer

`api/` — lowest layer. HTTP only, no business logic.

## Structure

```
api/
  core/
    base_api_client.py   ← base client, logging, Allure attachments
  users.py               ← domain API clients
  posts.py
  comments.py
  todos.py
```

## Class structure

```python
from api.core.base_api_client import BaseAPIClient
from config.settings import settings

class UsersAPI(BaseAPIClient):
    def __init__(self, token: str | None = None, base_url: str | None = None, **kwargs):
        super().__init__(base_url=base_url or settings.BASE_URL, **kwargs)
        if token:
            self.client.headers["Authorization"] = f"Bearer {token}"
```

- All clients inherit `BaseAPIClient` — logging and Allure attachments are free
- `api/core/` is infrastructure — domain clients do not live there
- `token` — Bearer auth, passed from outside
- Clients without auth (public read endpoints) pass `token=None`

## Routes

Module-level constants, never hardcode inside methods:

```python
USERS = "users"
USER_BY_ID = "users/{user_id}"
```

## Methods

```python
def get_users(self, page: int | None = None) -> httpx.Response:
    params = {"page": page} if page is not None else None
    return self.get(USERS, params=params)

def create_user(self, payload: dict) -> httpx.Response:
    return self.post(USERS, json=payload)

def delete_user(self, user_id: int) -> httpx.Response:
    return self.delete(USER_BY_ID.format(user_id=user_id))
```

- `json=` for JSON body
- `params=` for query params
- Always return `httpx.Response`
- Accept `dict` payload — Pydantic serialization happens in factories/services

## Context manager

```python
with UsersAPI(token=token) as api:
    return api.get_users()
```

## Allowed

- GET / POST / PUT / PATCH / DELETE
- Pass query params, body
- Return `httpx.Response`
- Know URL route constants
- Know headers / token

## Not allowed

- `assert_that`
- `allure.step`
- `response.raise_for_status()`
- Parse response into Pydantic model
- Generate test data
- `sleep` / retry logic
