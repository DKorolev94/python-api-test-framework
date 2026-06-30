---
paths:
  - "tests/**/*.py"
---

# Tests

Test is a scenario. Structure: Arrange → Act → Assert.

## Test structure

```python
@allure.feature("Users")
@pytest.mark.contract
class TestUsersPermissions:

    @linked(WorkItem(id=0, name="Users: create without token returns 401"))
    def test_create_user_no_token(self, users_api_no_auth: UsersAPI):
        with step("POST /users without token"):
            response = users_api_no_auth.create_user(create_user_payload_dict())
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
```

## Contract tests (`@pytest.mark.contract`)

Check HTTP contract. Work with `api/` directly.

Check:
- `status_code`
- Response structure (Pydantic validate)
- Required fields and their types
- Validation errors and error schema

Do not use:
- `service` layer
- Complex call chains
- Business flows

```python
@pytest.mark.contract
def test_create_user_invalid_email(self, users_api: UsersAPI):
    with step("POST /users with invalid email"):
        response = users_api.create_user(create_user_payload_dict(email="bad"))
    with step("Response: 422, email validation error"):
        assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))
        errors = [ValidationErrorItem.model_validate(e) for e in response.json()]
        assert_that([e.field for e in errors], has_item("email"))
```

## Integration tests (`@pytest.mark.integration`)

Check interaction of multiple parts. Work through `service/`.

Use:
- `service` layer
- factories
- helpers/checks
- Multiple API calls

```python
@pytest.mark.integration
def test_created_user_readable(self, user_service: UserService, created_user: UserResponse):
    with step("GET /users/{id} for created user"):
        fetched = user_service.get_user(created_user.id)
    with step("Fetched user matches created"):
        assert_that(fetched.id, equal_to(created_user.id))
```

## E2E tests (`@pytest.mark.e2e`)

Full user scenario. Real lifecycle, multiple entities.

Use:
- `service` layer
- Multiple entities and roles
- Cleanup via `try/finally`

## Positive tests → Pydantic payload

```python
payload = create_user_payload()
user = user_service.create_user(payload)
```

## Negative tests → raw dict

Pydantic model may refuse to create an invalid payload — test would fail before the request.

```python
payload = create_user_payload_dict(email="bad-email")
response = users_api.create_user(payload)
assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))
```

## Negative tests → api layer, not service

Service calls `raise_for_status()` — 4xx will throw. For error checks use `api/` directly.

```python
# Bad — service raises exception on 422
user_service.create_user(invalid_payload)

# Good — api returns raw response
response = users_api.create_user(invalid_payload_dict)
assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))
```

## File naming

Pattern: `test_<resource>.py` or `test_<resource>_<feature>.py`

```
tests/
  test_users.py
  test_posts.py
  test_comments.py
  test_todos.py
  test_e2e_blog_flow.py
```

## Class naming

| Class | When |
|---|---|
| `TestPermissions` | auth wall: no token → 401, invalid → 401 |
| `TestSchema` | schema validation: 422, missing fields |
| `TestCreate` / `TestUpdate` / `TestDelete` | CRUD happy path (integration) |
| `TestPagination` | page/per_page, no duplicates between pages |
| `TestByUser` / `TestByPost` | nested resource checks |

## Allure in tests

`@allure.feature` — required on every class.

```python
@allure.feature("Users")
@pytest.mark.contract
class TestUsersPermissions:
    ...
```

`step` — for logical Arrange / Act / Assert separation:

```python
with step("POST /users without token"):
    response = users_api.create_user(payload)

with step("Response: 401 Unauthorized"):
    assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
```

`@linked(WorkItem(...))` — required for TestIT linking.

## WorkItem naming

Pattern: `"Resource: scenario"` — resource first, scenario clarifies condition.

```python
@linked(WorkItem(id=0, name="Users: create without token returns 401"))
@linked(WorkItem(id=0, name="Users: create returns valid user with id"))
@linked(WorkItem(id=0, name="Users: pagination respects per_page limit"))
```

## Step naming

Step describes **what happens or what is checked**. No dashes (—, -) — use comma or space.

```python
# Bad
with step("Check 401"):
with step("Check response"):

# Good
with step("Response: 401 Unauthorized"):
with step("Response: 422, email validation error"):
with step("User created, id present"):
```

## Imports in tests

- `contract` tests: import `api/` + `factories/` + `models/responses/` (for schema check)
- `integration/e2e` tests: import `services/` + `factories/` + `helpers/`
