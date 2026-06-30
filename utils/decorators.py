import logging
import os
import tempfile
from collections import namedtuple
from functools import wraps

import allure
import testit

from config.settings import settings

logger = logging.getLogger(__name__)

_TESTCASE_URL = settings.TESTIT_URL

WorkItem = namedtuple("WorkItem", ["id", "name"])


def linked(*items: WorkItem, display_name: str | None = None):
    """Link test to TestIT work items and add Allure testcase links."""
    ids = [str(i.id) for i in items]
    if not ids:
        raise ValueError("linked() requires at least one WorkItem")
    external_id = f"AT{ids[0]}"

    def decorator(func):
        result = func
        for item in items:
            result = allure.testcase(name=item.name, url=_TESTCASE_URL.format(testit_id=item.id))(result)
        result = testit.workItemIds(*ids)(result)
        if display_name is not None:
            result = testit.displayName(display_name)(result)
        result = testit.externalId(external_id)(result)
        return result

    return decorator


def step(name_or_func=None):
    """Step in Allure and TestIT. Use as @step('name') or with step('name')."""
    if isinstance(name_or_func, str):
        return _Step(name_or_func)
    if callable(name_or_func):
        return _Step(name_or_func.__name__)(name_or_func)

    def decorator(func):
        return _Step(func.__name__)(func)
    return decorator


class _Step:
    def __init__(self, name: str):
        self.name = name
        self._testit_step = testit.step(name)
        self._allure_step = allure.step(name)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

    def __enter__(self):
        logger.info("Step: %s", self.name)
        self._testit_step.__enter__()
        self._allure_step.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._allure_step.__exit__(exc_type, exc_val, exc_tb)
        self._testit_step.__exit__(exc_type, exc_val, exc_tb)


def add_attachment(data: bytes, name: str = "attachment", is_text: bool = True) -> None:
    """Add attachment to Allure and TestIT."""
    ext = "txt" if is_text else "png"
    path = None
    with tempfile.NamedTemporaryFile(mode="wb", suffix=f".{ext}", delete=False) as f:
        f.write(data)
        path = f.name

    at_type = allure.attachment_type.TEXT if is_text else allure.attachment_type.PNG
    allure.attach(body=data, name=name, attachment_type=at_type)

    try:
        testit.addAttachments(data=path, name=name, is_text=is_text)
    except (SystemExit, IndexError):
        pass
    finally:
        if path:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
