---
paths:
  - "models/**/*.py"
---

# Models Layer

`models/` — Pydantic models for requests and responses. Pure data structures, no logic.

## Structure

```
models/
  requests/    → CreateUserRequest, UpdatePostRequest, ...
  responses/   → UserResponse, PostResponse, PaginationMeta, ...
    common.py  → shared: PaginationMeta, GoRestError, ValidationErrorItem
```

## Request model pattern

```python
from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str   # "male" | "female"
    status: str = "active"
```

## Response model pattern

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    gender: str
    status: str
```

## GoRest error models (in common.py)

```python
class GoRestError(BaseModel):
    message: str              # 401, 404

class ValidationErrorItem(BaseModel):
    field: str                # 422 — list of these
    message: str
```

## Pagination (GoRest uses response headers)

```python
class PaginationMeta(BaseModel):
    total: int
    pages: int
    page: int
    limit: int
```

## Naming

- Request: `*Request` — `CreateUserRequest`, `UpdatePostRequest`
- Response: `*Response` — `UserResponse`, `PostResponse`
- Error: `GoRestError`, `ValidationErrorItem`
- Nested sub-models: `*Meta`, `*Options`, `*Base`

## Allowed

- Pydantic `BaseModel`
- `EmailStr`, `field_validator`
- Nested models
- `| None` for optional fields
- Default values

## Not allowed

- Import `httpx`, `api/`, `services/`, `factories/`, `helpers/`, `fixtures/`
- HTTP requests
- Business logic
- `assert_that`
- `allure.step`
