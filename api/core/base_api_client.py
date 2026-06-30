import json
from http import HTTPStatus

import allure
import httpx
from httpx import Response

from utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 30
DEFAULT_HEADERS = {"Accept": "application/json"}


class BaseAPIClient:
    """Base HTTP client with Allure attachments and request/response logging."""

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

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        logger.info(f"{method} {url}")
        if "json" in kwargs:
            logger.debug(f"Request body: {kwargs['json']}")
        if "params" in kwargs:
            logger.debug(f"Request params: {kwargs['params']}")

    def _attach_request(self, method: str, url: str, **kwargs) -> None:
        info = {"method": method, "url": url}
        if "params" in kwargs:
            info["params"] = kwargs["params"]
        allure.attach(
            json.dumps(info, ensure_ascii=False, indent=2, default=str),
            name="Request Info",
            attachment_type=allure.attachment_type.JSON,
        )
        body = kwargs.get("json")
        if body is not None:
            allure.attach(
                json.dumps(body, ensure_ascii=False, indent=2, default=str),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON,
            )

    def _attach_response(self, response: Response) -> None:
        allure.attach(
            json.dumps({"status_code": response.status_code}, indent=2),
            name="Response Info",
            attachment_type=allure.attachment_type.JSON,
        )
        try:
            body = response.json()
        except Exception:
            body = response.text
        allure.attach(
            json.dumps(body, ensure_ascii=False, indent=2, default=str),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

    def _log_response(self, response: Response) -> None:
        logger.info(f"Response {response.status_code}")
        if response.status_code >= HTTPStatus.BAD_REQUEST:
            logger.info(f"Response body: {response.text}")
        else:
            logger.debug(f"Response body: {response.text[:200]}")

    def request(self, method: str, endpoint: str, **kwargs) -> Response:
        headers = kwargs.pop("headers", {})
        kwargs["headers"] = {**self._default_headers, **headers}
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}" if self.base_url else endpoint

        self._log_request(method, url, **kwargs)
        self._attach_request(method, url, **kwargs)

        try:
            response = self.client.request(method, endpoint, **kwargs)
            self._log_response(response)
            self._attach_response(response)
            return response
        except httpx.RequestError as e:
            logger.error(f"Request error {method} {url}: {e}")
            raise

    def get(self, endpoint: str, **kwargs) -> Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self.request("DELETE", endpoint, **kwargs)

    def close(self) -> None:
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
