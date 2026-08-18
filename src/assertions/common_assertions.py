from typing import Any

import allure


def assert_equal(actual: Any, expected: Any, description: str) -> None:
    """Проверяет, что значения равны. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert actual == expected, f"ожидалось {expected}, получено {actual}"


def assert_not_equal(actual: Any, expected: Any, description: str) -> None:
    """Проверяет, что значения не равны. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert actual != expected, f"значение не должно было быть {expected}, но оказалось именно таким"


def assert_in(item: Any, collection: Any, description: str) -> None:
    """Проверяет, что элемент есть в коллекции. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert item in collection, f"{item} не найден в {collection}"


def assert_not_in(item: Any, collection: Any, description: str) -> None:
    """Проверяет, что элемента нет в коллекции. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert item not in collection, f"{item} неожиданно найден в {collection}"


def assert_not_empty(collection: Any, description: str) -> None:
    """Проверяет, что коллекция не пустая. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert len(collection) > 0, "коллекция оказалась пустой"


def assert_greater(actual: Any, threshold: Any, description: str) -> None:
    """Проверяет, что значение больше порога. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert actual > threshold, f"ожидалось больше {threshold}, получено {actual}"


def assert_true(condition: bool, description: str) -> None:
    """Проверяет, что условие истинно. Обёрнуто в шаг Allure."""
    with allure.step(f"Проверить, что {description}"):
        assert condition, "условие не выполнено"
