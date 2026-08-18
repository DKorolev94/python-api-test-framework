# python-api-test-framework

Портфолио-проект: как я строю фреймворк для API-тестов. Структура повторяет мой рабочий проект (mymood-api-tests), только API тут публичное, GoRest (пользователи, посты, комментарии, задачи).

## Стек

- Python 3.12, pytest
- httpx: HTTP клиент
- Pydantic v2: модели запросов и ответов
- Faker: генерация тестовых данных
- Allure: отчёты и ассерты
- Docker Compose: прогон тестов и живой отчёт локально
- ruff: линтер

## Структура

```
src/
├── api/
│   ├── base_api_client.py   базовый HTTP клиент
│   ├── routes.py             роуты по ресурсам
│   ├── clients/               HTTP клиенты, отдают только httpx.Response
│   └── services/               бизнес-логика, отдают Pydantic модели
├── assertions/                assert_status_code, assert_equal и т.д.
├── models/requests, responses  модели запросов и ответов
├── factories/                  сборка тестовых данных
├── helpers/                    проверки над списками объектов
├── database/                   коннектор к Postgres, для примера архитектуры (к GoRest база не подключена)
└── config/                     настройки, пути
fixtures/                      подготовка и очистка тестовых данных
tests/
├── users/, posts/, comments/, todos/   тесты по ресурсам
└── e2e/                                  сквозные сценарии
```

## Установка

```bash
git clone https://github.com/your-username/python-api-test-framework.git
cd python-api-test-framework
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# в .env вписать GOREST_TOKEN (взять на https://gorest.co.in/my-account/access-tokens)
```

## Запуск тестов

```bash
python -m pytest tests/ -v

python -m pytest -m contract -v
python -m pytest -m integration -v
python -m pytest -m e2e -v

# с отчётом Allure
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results

ruff check .
```

## Через Docker с живым отчётом

```bash
docker-compose up --build
```

Отчёт на `http://localhost:5050`, обновляется сам по мере прогона. Остановить: `Ctrl+C`. Запустить с другими параметрами:

```bash
docker-compose run --rm api-test-runner -m contract -v
```

Только локально, без Allure TestOps и CI.

## Маркеры

| Маркер | Что покрывает |
|---|---|
| `contract` | схема, коды ответов, авторизация |
| `integration` | CRUD, пагинация, вложенные ресурсы |
| `e2e` | сквозные сценарии (юзер → пост → комментарий → удаление) |
| `smoke` | только критичный путь |
| `db` | демо слоя БД, реально не подключён |
