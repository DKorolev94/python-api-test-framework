---
# Comments & Docstrings

Comments and docstrings — only when name + types don't explain the behavior.

## Where docstrings are required

### `helpers/` — always

Pure data analysis functions. Docstring is required: return value, filter condition, exception if any.

```python
def get_first_user_id(users: list[UserResponse]) -> int:
    """Returns id of the first user. Raises ValueError if list is empty."""
    if not users:
        raise ValueError("users list is empty")
    return users[0].id

def all_users_active(users: list[UserResponse]) -> bool:
    """True if all users have status 'active'."""
    return bool(users) and all(u.status == "active" for u in users)
```

### `utils/` — only for non-obvious behavior

If function creates a file, formats by non-standard format, has side effects — docstring needed. Simple data generators — no.

```python
# Needed — non-obvious: specific format + rounding
def future_datetime(hours_ahead: int = 24) -> str:
    """ISO 8601: now + N hours, rounded to hour."""

# Not needed — name says it all
def random_email() -> str:
    ...
```

### Public decorators — usage modes

If function is used in multiple ways (decorator and context manager) — docstring describes this.

```python
def step(name_or_func=None):
    """Step in Allure and TestIT. Use as @step('name') or with step('name')."""
```

## Where docstrings are NOT needed

| Layer | Reason |
|---|---|
| `api/` | Thin HTTP wrappers. Method name + types are sufficient |
| `services/` | Typed Pydantic params + return type = documentation |
| `factories/` | Factory name is obvious |
| `fixtures/` | pytest fixture — name = purpose |
| `tests/` | Test methods are not documented |
| `models/` | Pydantic fields are self-documenting |

## Format

One line, English. No parameter description — types are already in the signature.

```python
# Good
"""Returns id of the first user. Raises ValueError if list is empty."""

# Bad — restates the name
"""Gets the first user from the list of users."""

# Bad — params are already visible in the signature
"""
Args:
    users: list of users
Returns:
    id of the first user
"""
```

## Inline comments

Only when WHY is non-obvious — hidden constraint, bug workaround, surprising behavior.

```python
# Good — explains non-obvious side effect
r, g, b = os.urandom(3)  # unique bytes → different PNG hash on each call

# Bad — restates the code
result = func  # assign func to result variable
```
