---
paths:
  - "steps/**/*.py"
---

# Steps Layer

`steps/` — optional wrapper with `@allure.step` for frequently repeated actions.

## Principle

Step class wraps service calls in Allure steps. No logic — only delegation.

## Class structure

```python
import allure

from models.requests.user import CreateUserRequest
from models.responses.user import UserResponse
from services.user_service import UserService


class UserSteps:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @allure.step("Create user")
    def create_user(self, payload: CreateUserRequest) -> UserResponse:
        return self.user_service.create_user(payload)

    @allure.step("Delete user")
    def delete_user(self, user_id: int) -> None:
        return self.user_service.delete_user(user_id)
```

## When to create steps/

If the same action with an Allure step repeats in 3+ tests.

If the step is one-off — write directly in test:

```python
with step("Create user"):
    user = user_service.create_user(create_user_payload())
```

## Allowed

- Wrap service calls in `@allure.step`
- Accept and pass through payload/models
- Return whatever the service returns

## Not allowed

- Business logic
- Make direct API requests (only via service)
- `assert_that`
- Generate payload / call factories
- `response.raise_for_status()`
