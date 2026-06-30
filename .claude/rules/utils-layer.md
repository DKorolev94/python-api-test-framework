---
paths:
  - "utils/**/*.py"
---

# Utils Layer

`utils/` — reusable utilities: data generators, decorators, logging.

## Structure

```
utils/
  data_generators.py   → DataGenerator (email, name, sentences, dates)
  decorators.py        → linked, step, add_attachment (Allure + TestIT)
  logger.py            → configure_logging, get_logger
```

## DataGenerator

Static class. Data generation only, no requests:

```python
class DataGenerator:
    @staticmethod
    def random_email() -> str: ...
    @staticmethod
    def random_full_name() -> str: ...
    @staticmethod
    def random_sentence(nb_words: int = 6) -> str: ...
    @staticmethod
    def random_paragraph(nb_sentences: int = 3) -> str: ...
    @staticmethod
    def future_datetime(hours_ahead: int = 24) -> str: ...
```

Uses `Faker` for random data.

## Decorators

### `linked(*items: WorkItem, display_name=None)`

Links test to TestIT + Allure. `WorkItem = namedtuple("WorkItem", ["id", "name"])`:

```python
@linked(WorkItem(id=1234, name="Users: create returns valid user"))
def test_create_user(self, created_user: UserResponse):
    ...
```

### `step("description")`

Step in Allure and TestIT. Use as decorator or context manager:

```python
@step("Create user")
def create_user(): ...

with step("Response: 200 OK"):
    assert_that(...)
```

### `add_attachment(data, name, is_text=True)`

Attachment in Allure and TestIT.

## Logger

```python
def configure_logging(level="INFO", http_client_level="WARNING"): ...
def get_logger(name) -> Logger: ...
```

httpx/httpcore — WARNING by default. Format: `HH:MM:SS [LEVEL] name: message`.

## Allowed

- Generate random test data
- Use `Faker`, `random`, `uuid`
- Log via `logging`
- Configure Allure/TestIT decorators
- Read `config.settings`

## Not allowed

- Make API requests
- Make DB queries
- `assert_that`
- Create Pydantic request/response models
- Test logic
- Import `api/`, `services/`, `factories/`, `fixtures/`, `tests/`
