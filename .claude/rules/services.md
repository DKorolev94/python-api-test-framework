---
paths:
  - "services/**/*.py"
---

# Service Layer

`services/` — business action layer. Calls API, checks HTTP status, returns Pydantic model.

## Principle

Service is the only place where `httpx.Response` becomes a domain object.

## Class structure

```python
class UserService:
    def __init__(self, users_api: UsersAPI):
        self.users_api = users_api
```

API client is injected via `__init__`. Service never creates an API client itself.

## Basic method pattern

```python
def create_user(self, payload: CreateUserRequest) -> UserResponse:
    response = self.users_api.create_user(payload.model_dump(mode="json"))
    response.raise_for_status()
    return UserResponse.model_validate(response.json())
```

## List pattern

```python
def get_users(self, page: int | None = None) -> list[UserResponse]:
    response = self.users_api.get_users(page=page)
    response.raise_for_status()
    return [UserResponse.model_validate(u) for u in response.json()]
```

## Pagination pattern (GoRest returns meta in headers)

```python
def get_page(self, page: int | None = None, per_page: int | None = None) -> tuple[list[UserResponse], PaginationMeta]:
    response = self.users_api.get_users(page=page, per_page=per_page)
    response.raise_for_status()
    users = [UserResponse.model_validate(u) for u in response.json()]
    meta = PaginationMeta(
        total=int(response.headers.get("X-Pagination-Total", 0)),
        pages=int(response.headers.get("X-Pagination-Pages", 1)),
        page=int(response.headers.get("X-Pagination-Page", 1)),
        limit=int(response.headers.get("X-Pagination-Limit", 10)),
    )
    return users, meta
```

## Allowed

- Call API methods
- `response.raise_for_status()`
- Return Pydantic response models
- Combine multiple API calls into one business action
- Accept ready payload / request model
- Return `None` for void operations (delete)
- Raise `ValueError` if entity not found

## Not allowed

- Import `factories`
- Generate payload inside service
- `allure.step`
- `assert_that`
- Accept or return `httpx.Response` externally
- Contain polling / sleep / wait
- Mutate incoming payload
