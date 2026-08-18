import json
from http import HTTPStatus

import allure
import httpx
from httpx import Response

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 30
DEFAULT_HEADERS = {"Accept": "application/json"}

SENSITIVE_KEYS = {"password", "token"}
MASK = "******"


def _mask(value):
    """Рекурсивно заменяет чувствительные поля (password, token) на маску для безопасного логирования."""
    if isinstance(value, dict):
        return {k: MASK if any(s in k.lower() for s in SENSITIVE_KEYS) else _mask(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_mask(v) for v in value]
    return value


def _log_and_attach_request(method: str, url: str, **kwargs) -> None:
    """Логирует и прикладывает в Allure замаскированный снимок исходящего запроса."""
    body = kwargs.get("json")
    params = kwargs.get("params")

    logger.info(f"{method} {url}")
    if body is not None:
        logger.debug(f"Request body: {_mask(body)}")
    if params:
        logger.debug(f"Request params: {_mask(params)}")

    info = {"method": method, "url": url}
    if params:
        info["params"] = _mask(params)
    allure.attach(
        json.dumps(info, ensure_ascii=False, indent=2, default=str),
        name="Request Info",
        attachment_type=allure.attachment_type.JSON,
    )
    if body is not None:
        allure.attach(
            json.dumps(_mask(body), ensure_ascii=False, indent=2, default=str),
            name="Request Body",
            attachment_type=allure.attachment_type.JSON,
        )


def _log_and_attach_response(response: Response) -> None:
    """Логирует и прикладывает в Allure замаскированный снимок ответа."""
    try:
        body = _mask(response.json())
    except json.JSONDecodeError:
        body = response.text

    logger.info(f"Response {response.status_code}")
    if response.status_code >= HTTPStatus.BAD_REQUEST:
        logger.info(f"Response body: {body}")
    else:
        logger.debug(f"Response body: {str(body)[:200]}")

    allure.attach(
        json.dumps({"status_code": response.status_code}, indent=2),
        name="Response Info",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        json.dumps(body, ensure_ascii=False, indent=2, default=str),
        name="Response Body",
        attachment_type=allure.attachment_type.JSON,
    )


def pagination_params(page: int | None = None, per_page: int | None = None) -> dict:
    """Собирает словарь query-параметров из page и per_page, пропуская незаданные значения."""
    params = {}
    if page is not None:
        params["page"] = page
    if per_page is not None:
        params["per_page"] = per_page
    return params


class BaseAPIClient:
    """Базовый HTTP клиент с логированием запросов и ответов и вложениями в Allure."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        default_headers: dict[str, str] | None = None,
    ):
        self.base_url = base_url
        self._default_headers = default_headers or DEFAULT_HEADERS
        self.client = httpx.Client(
            base_url=self.base_url or "",
            timeout=timeout,
            headers=self._default_headers,
        )

    def request(self, method: str, endpoint: str, **kwargs) -> Response:
        """Отправляет HTTP запрос и логирует его вместе с ответом."""
        headers = kwargs.pop("headers", {})
        kwargs["headers"] = {**self._default_headers, **headers}
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}" if self.base_url else endpoint

        _log_and_attach_request(method, url, **kwargs)

        try:
            response = self.client.request(method, endpoint, **kwargs)
        except httpx.RequestError:
            logger.exception(f"Request error {method} {url}")
            raise
        else:
            _log_and_attach_response(response)
            return response

    def get(self, endpoint: str, **kwargs) -> Response:
        """Отправляет GET запрос на указанный endpoint."""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        """Отправляет POST запрос на указанный endpoint."""
        return self.request("POST", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        """Отправляет PATCH запрос на указанный endpoint."""
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        """Отправляет DELETE запрос на указанный endpoint."""
        return self.request("DELETE", endpoint, **kwargs)

    def close(self) -> None:
        """Закрывает внутренний HTTP клиент."""
        self.client.close()

    def __enter__(self):
        """Входит в контекстный менеджер."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает клиента при выходе из контекстного менеджера."""
        self.close()


class AuthenticatedAPIClient(BaseAPIClient):
    """Базовый клиент для ресурсов, которым нужен bearer токен."""

    def __init__(self, token: str | None = None, base_url: str | None = None, **kwargs):
        super().__init__(base_url=base_url or settings.BASE_URL, **kwargs)
        if token:
            self.client.headers["Authorization"] = f"Bearer {token}"
