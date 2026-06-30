---
paths:
  - "fixtures/**/*.py"
---

# Fixtures

`fixtures/` — pytest fixtures for setup/teardown of test data and infrastructure.

## Principle

Fixture provides a ready entity or client. Tests must not create them manually.

## API client + service pattern

```python
@pytest.fixture
def users_api(api_token: str) -> Generator[UsersAPI, None, None]:
    with UsersAPI(token=api_token) as api:
        yield api

@pytest.fixture
def user_service(users_api: UsersAPI) -> UserService:
    return UserService(users_api)
```

## Entity creation with teardown

```python
@pytest.fixture
def created_user(user_service: UserService) -> Generator[UserResponse, None, None]:
    user = user_service.create_user(create_user_payload())
    yield user
    user_service.delete_user(user.id)
```

## Scopes

| Scope | When to use |
|---|---|
| `session` | tokens, expensive shared resources |
| `function` | new entity per test, API clients |

```python
@pytest.fixture(scope="session")
def api_token() -> str:
    return settings.GOREST_TOKEN

@pytest.fixture
def created_user(user_service: UserService) -> Generator[UserResponse, None, None]:
    user = user_service.create_user(create_user_payload())
    yield user
    user_service.delete_user(user.id)
```

## Fixture naming

| Prefix | Scope | When |
|---|---|---|
| `created_` | `session` | one entity for entire session, shared between tests |
| `fresh_` | `function` | new entity per test |

## indirect parametrization

```python
@pytest.fixture
def user_with_status(request, user_service: UserService) -> UserResponse:
    return user_service.create_user(create_user_payload(status=request.param))

@pytest.mark.parametrize("user_with_status", ["active", "inactive"], indirect=True)
def test_user_status(self, user_with_status: UserResponse):
    ...
```

## Allowed

- Create API clients and services
- Create test entities via service
- Cleanup via `yield`
- Read from `settings`
- Accept parameters via `request.param` (indirect)

## Not allowed

- `assert_that`
- Test logic inside fixture
- Cleanup in `session`-scoped fixtures if entity is shared across tests
