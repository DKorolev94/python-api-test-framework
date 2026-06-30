---
paths:
  - "assertions/**/*.py"
---

# Assertions Layer

`assertions/` — reusable checks for tests. Extract here when the same check repeats in 2+ tests.

## Principle

Assertion helper accepts a ready response model, calls `assert_that`, returns `None`.
Do not accept `httpx.Response` — only Pydantic models.

## Base pattern

```python
from hamcrest import assert_that, equal_to, not_, empty

from helpers.user_checks import all_users_active
from models.responses.user import UserResponse


def assert_all_users_active(users: list[UserResponse]) -> None:
    assert_that(users, not_(empty()))
    assert_that(all_users_active(users), equal_to(True))
```

## Patterns

### Field check

```python
def assert_user_created(user: UserResponse) -> None:
    assert_that(user.id, instance_of(int))
    assert_that(user.status, equal_to("active"))
    assert_that(user.name, not_(none()))
```

### Error response check

```python
def assert_validation_error_on_field(errors: list[ValidationErrorItem], field: str) -> None:
    assert_that([e.field for e in errors], has_item(field))
```

## Conventions

- Name: `assert_<what_we_check>` — `assert_user_created`, `assert_validation_error_on_field`
- One file per domain: `user_assertions.py`, `post_assertions.py`
- Check data is not empty first, then check content
- Extract complex condition logic to `helpers/`, not inline in `assert_that`

## Anti-pattern: boolean eval before hamcrest

```python
# Bad — Python evaluates bool before hamcrest; report shows True/False not real value
assert_that(user_id in ids, equal_to(True))

# Good — hamcrest shows what was expected and what was received
assert_that(ids, has_item(user_id))
```

## When to extract to assertions/

Extract if check repeats in 2+ tests. If used once — write `assert_that` inline in test.

## Allowed

- `assert_that` from PyHamcrest
- Accept Pydantic response models
- Use check functions from `helpers/`

## Not allowed

- Make API requests
- Create payload or factories
- Call services
- Create or delete entities
- Accept `httpx.Response`
- `allure.step`
