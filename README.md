# python-api-test-framework

Portfolio project demonstrating production-grade API test automation architecture.

**API under test:** [GoRest](https://gorest.co.in) — public REST API (users, posts, comments, todos)

## Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Language |
| pytest | Test runner |
| httpx | HTTP client |
| Pydantic v2 | Request/response models |
| Faker | Test data generation |
| PyHamcrest | Assertions |
| Allure | Test reporting |
| TestIT | Test management system |
| ruff | Linter |

## Architecture

```
api/        → HTTP clients (httpx.Response only)
services/   → business logic (return Pydantic models)
factories/  → payload builders (Faker-based)
helpers/    → pure analysis functions
fixtures/   → pytest setup/teardown
tests/      → contract / integration / e2e
database/   → PostgreSQL stub (used when API is insufficient)
```

Each layer has strict rules — see [`.claude/rules/`](.claude/rules/).

## Setup

```bash
# 1. Clone and create venv
git clone https://github.com/your-username/python-api-test-framework.git
cd python-api-test-framework
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env — set GOREST_TOKEN (get at https://gorest.co.in/my-account/access-tokens)
```

## Run tests

```bash
# All tests
python -m pytest tests/ -v

# By marker
python -m pytest -m contract -v
python -m pytest -m integration -v
python -m pytest -m e2e -v

# With Allure report
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results

# Lint
ruff check .
```

## Test markers

| Marker | Description |
|---|---|
| `contract` | Schema validation, status codes, auth checks |
| `integration` | CRUD flows, pagination, nested resources |
| `e2e` | Full user scenarios (user → post → comment → cleanup) |
| `smoke` | Critical path only |

## Project structure

```
python-api-test-framework/
├── api/
│   ├── core/base_api_client.py
│   ├── users.py
│   ├── posts.py
│   ├── comments.py
│   └── todos.py
├── models/
│   ├── requests/          # CreateUserRequest, UpdatePostRequest, ...
│   └── responses/         # UserResponse, PostResponse, PaginationMeta, ...
├── services/              # UserService, PostService, ...
├── factories/             # create_user_payload(), create_post_payload(), ...
├── helpers/               # user_checks.py, post_checks.py, pagination_checks.py
├── fixtures/              # auth.py, user.py, post.py, comment.py, todo.py
├── database/              # PostgreSQL connector stub
├── utils/                 # logger, data_generators, decorators
├── config/                # settings.py (pydantic-settings), paths.py
├── tests/
│   ├── test_users.py
│   ├── test_posts.py
│   ├── test_comments.py
│   ├── test_todos.py
│   └── test_e2e_blog_flow.py
├── CLAUDE.md
└── .claude/rules/         # 14 architectural rule files
```

## Key design decisions

**Layer isolation:** `api/` returns only `httpx.Response`. Services parse into Pydantic models. Tests use services for positive flows and api clients directly for negative/error scenarios.

**Two factory versions:** `create_user_payload()` returns a Pydantic model (positive tests), `create_user_payload_dict()` returns a raw dict (negative tests with invalid data).

**Fixtures with teardown:** All created entities are cleaned up via `yield` fixtures, keeping the API environment clean between runs.

**Pagination via headers:** GoRest returns pagination metadata in response headers (`X-Pagination-Total`, `X-Pagination-Pages`, etc.), not in the response body.
