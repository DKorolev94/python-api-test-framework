---
paths:
  - "factories/**/*.py"
---

# Factories

`factories/` — payload builders for tests. No logic, only data.

## Principle

Factory is a pure function. Accepts overrides, returns filled model or dict.

## Base pattern

```python
from typing import Any
from models.requests.user import CreateUserRequest
from utils.data_generators import DataGenerator

def create_user_payload(**overrides: Any) -> CreateUserRequest:
    data = {
        "name": DataGenerator.random_full_name(),
        "email": DataGenerator.random_email(),
        "gender": "male",
        "status": "active",
    }
    data.update(overrides)
    return CreateUserRequest(**data)

def create_user_payload_dict(**overrides: Any) -> dict[str, Any]:
    data = create_user_payload().model_dump(mode="json")
    data.update(overrides)
    return data
```

## Two-version rule

Every important request model needs two functions:

| Function | Returns | Used for |
|---|---|---|
| `create_user_payload()` | Pydantic request model | positive tests, services |
| `create_user_payload_dict()` | raw dict | negative tests, invalid data |

```python
# Positive — through service
payload = create_user_payload()
user = user_service.create_user(payload)

# Negative — dirty dict directly to API
payload = create_user_payload_dict(email="not-an-email")
response = users_api.create_user(payload)
```

## Required params as explicit args

```python
def create_post_payload(user_id: int, **overrides: Any) -> CreatePostRequest:
    data = {
        "user_id": user_id,
        "title": DataGenerator.random_sentence(),
        "body": DataGenerator.random_paragraph(),
    }
    data.update(overrides)
    return CreatePostRequest(**data)
```

## Allowed

- Create valid Pydantic request models
- Create raw dict via `.model_dump(mode="json")`
- Generate random data (`DataGenerator`)
- Accept `**overrides`
- Read constants from `settings`

## Not allowed

- Make HTTP requests
- `assert_that`
- `allure.step`
- Create services or API clients
- Check responses
- Cleanup / teardown
- Business logic
