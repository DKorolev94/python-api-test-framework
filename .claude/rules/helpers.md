---
paths:
  - "helpers/**/*.py"
---

# Helpers / Checks

`helpers/` — pure functions for analyzing ready response models. No requests, only data.

## Principle

Helper accepts a Pydantic response model, returns a primitive type. No side effects.

## Patterns

### Extract value

```python
def get_first_user_id(users: list[UserResponse]) -> int:
    """Returns id of the first user. Raises ValueError if list is empty."""
    if not users:
        raise ValueError("users list is empty")
    return users[0].id
```

### Boolean all/any check

```python
def all_users_active(users: list[UserResponse]) -> bool:
    """True if all users have status 'active'."""
    return bool(users) and all(u.status == "active" for u in users)
```

### Set of IDs

```python
def user_ids(users: list[UserResponse]) -> set[int]:
    """Returns set of all user IDs."""
    return {u.id for u in users}
```

## Conventions

- Function name describes what it checks: `all_*`, `get_first_*`, `*_ids`
- Empty list → `False` for `all_*` functions (`bool(items) and all(...)`)
- Empty list → `ValueError` for `get_*` functions
- One file per domain area: `user_checks.py`, `post_checks.py`
- Always add docstring — describes return value, filter condition, exception if any

## Difference: check vs assertion

```python
# check — returns bool, test decides what to do with it
def all_users_active(users: list[UserResponse]) -> bool:
    return bool(users) and all(u.status == "active" for u in users)

# assertion — calls assert_that, lives in test or assertions module
assert_that(all_users_active(users), equal_to(True))
```

## Allowed

- Accept Pydantic response model
- Return `bool`, `str`, `int`, `list`, `set`
- `all(...)` / `any(...)` over collection
- Extract IDs, counters, flags from model
- Raise `ValueError` if data is absent

## Not allowed

- Make API requests
- Create payload or factories
- `allure.step`
- `assert_that` (that's an assertion, not a check)
- Call services
- Side effects
