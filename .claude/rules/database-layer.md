---
paths:
  - "database/**/*.py"
---

# Database Layer

`database/` — PostgreSQL connector with optional SSH tunnel and direct SQL queries.
**Use only when data cannot be obtained via API.**

## Structure

```
database/
  connectors/
    postgres_connector.py   → DatabaseConnector (SSH), DatabaseManager (cursor)
  queries/
    db_operations.py        → DBOperation (domain queries)
  exceptions.py             → DatabaseConnectionError
```

## DatabaseConnector

Optional SSH tunnel + psycopg2 connection.

```python
class DatabaseConnector:
    def connect(self):
        if settings.DB_SSH_HOST:
            self.tunnel = SSHTunnelForwarder(...)
            self.tunnel.start()
        self.connection = psycopg2.connect(...)
        return self.connection

    def close(self): ...
```

All settings from `config.settings`.

## DatabaseManager

Cursor wrapper:

```python
class DatabaseManager:
    def execute(self, query: str, params: tuple | None = None) -> None: ...
    def fetchone(self): ...
    def fetchall(self): ...
    def commit(self): ...
    def rollback(self): ...
```

## DBOperation

Domain-specific queries. Each method is one operation:

```python
class DBOperation:
    def get_user_by_email(self, email: str) -> dict | None:
        """Returns user row by email, or None if not found."""
        self.db_manager.execute(
            "SELECT id, name, email, status FROM users WHERE email = %s LIMIT 1",
            (email,),
        )
        row = self.db_manager.fetchone()
        ...
```

## Conventions

- **Params via `%s`**, never f-strings in SQL
- After write — `commit()`, on error — `rollback()`
- Exceptions: log via `logger` and raise `RuntimeError`
- Accepts `db_manager` via `__init__`, never creates it itself

## Allowed

- Use `psycopg2` directly
- Use `sshtunnel`
- Read settings from `config.settings`
- `commit()` / `rollback()`
- Log SQL queries
- Raise `RuntimeError` / `DatabaseConnectionError`

## Not allowed

- Make HTTP API requests
- `assert_that`
- `allure.step`
- Generate test data
- Use f-strings in SQL queries
