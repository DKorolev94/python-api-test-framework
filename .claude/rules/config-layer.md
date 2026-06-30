---
paths:
  - "config/**/*.py"
---

# Config Layer

`config/` — settings via pydantic-settings and path constants. Single source of configuration for all layers.

## Structure

```
config/
  settings.py   → Settings (pydantic-settings), get_settings(), settings
  paths.py      → Path constants (ROOT, RESOURCES)
```

## Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    ENVIRONMENT: str
    BASE_URL: str
    GOREST_TOKEN: str
    LOG_LEVEL: str = "INFO"
    TESTIT_URL: str = "https://testit.example.com/projects/1/tests/{testit_id}"

    # Database (optional)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "testdb"
    DB_USER: str = "testuser"
    DB_PASSWORD: str = "testpassword"
```

Required fields have no default. Optional fields have explicit defaults.

## Paths

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "resources"
```

Only Path constants. No logic.

## Allowed

- Define Settings fields with type annotations
- Use `pydantic_settings.BaseSettings`
- Set default values
- Load `.env` via `python-dotenv`
- Store Path constants in `paths.py`

## Not allowed

- Import `httpx`, `api/`, `services/`, `factories/`, `models/`, `database/`
- Business logic
- HTTP requests
- Store secrets in code (only in `.env`)
- Compute values from other settings
