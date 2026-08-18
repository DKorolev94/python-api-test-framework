from http import HTTPStatus

import allure
import httpx
from pydantic import BaseModel, ValidationError


@allure.step("Проверить код ответа")
def assert_status_code(response: httpx.Response, expected: HTTPStatus) -> None:
    """Проверяет, что код ответа совпадает с ожидаемым."""
    assert response.status_code == expected, (
        f"ожидался код {expected.value} {expected.phrase}, получен {response.status_code} {response.reason_phrase}"
    )


@allure.step("Проверить, что тело ответа соответствует схеме")
def assert_schema_valid(response: httpx.Response, model: type[BaseModel]) -> BaseModel:
    """Проверяет, что тело ответа проходит валидацию по модели Pydantic."""
    try:
        return model.model_validate(response.json())
    except ValidationError as e:
        message = f"тело ответа не соответствует схеме {model.__name__}: {e}"
        raise AssertionError(message) from e


@allure.step("Проверить, что каждый элемент списка соответствует схеме")
def assert_list_schema_valid(response: httpx.Response, model: type[BaseModel]) -> list[BaseModel]:
    """Проверяет, что тело ответа это список и каждый элемент проходит валидацию по модели."""
    data = response.json()
    assert isinstance(data, list), f"ответ должен быть списком, получен {type(data).__name__}"
    try:
        return [model.model_validate(item) for item in data]
    except ValidationError as e:
        message = f"элемент списка не соответствует схеме {model.__name__}: {e}"
        raise AssertionError(message) from e
