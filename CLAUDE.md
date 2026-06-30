# python-api-test-framework

API test automation framework. Python + pytest + httpx + Allure + TestIT.
Layer rules — `.claude/rules/`.

## Layers

```
api/        → HTTP clients, return httpx.Response only
services/   → business logic, return Pydantic models
factories/  → payload builders (Faker-based)
helpers/    → pure analysis functions
fixtures/   → pytest setup/teardown
tests/      → contract / integration / e2e
```

## Where to add

| Situation | Where |
|---|---|
| New endpoint | `api/<resource>.py` + route constant there |
| Business logic / response parsing | `services/<resource>_service.py` |
| Request / response structure | `models/requests/` or `models/responses/` |
| Reusable test preset | `fixtures/<resource>.py` |
| Payload builder | `factories/<resource>.py` |
| Response model analysis | `helpers/<resource>_checks.py` |
| Database access | `database/queries/db_operations.py` |

## Conventions

- Assertions: **PyHamcrest** (`assert_that`, `equal_to`, `not_`, `empty`, ...)
- Status codes: `http.HTTPStatus`, not raw numbers
- TestIT linking: `@linked(WorkItem(id=..., name=...))` on every test method

## Run

```bash
python -m pytest tests/ -v
python -m pytest -m contract -v
python -m pytest -m integration -v
python -m pytest -m e2e -v
ruff check .
```

## Database

Use only when data cannot be obtained via API:
- `db.get_user_by_email(email)`
- `db.set_user_status(user_id, status)`
