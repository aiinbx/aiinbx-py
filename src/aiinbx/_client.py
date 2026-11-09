from __future__ import annotations

import email.utils
import os
import random
import time
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, cast

import httpx
from typing_extensions import Unpack

from ._base import RawResponse
from ._errors import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from ._generated.client import (
    AsyncRawResources,
    AsyncResources,
    RawResources,
    Resources,
    SharedHeaders,
    shared_headers,
)
from ._version import __version__
from ._webhooks import Webhooks

DEFAULT_BASE_URL = "https://api.aiinbx.com/api/v2"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2
# Worth another try when sending twice cannot act twice; a 429 always is.
_RETRY_STATUSES = {408}
# Methods that act the same however often they are sent.
_IDEMPOTENT_METHODS = {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}


def _request_id(headers: Mapping[str, str]) -> str | None:
    return headers.get("x-request-id") or headers.get("request-id")


def _response_request_id(response: httpx.Response, body: Any = None) -> str | None:
    header_id = _request_id(response.headers)
    if header_id:
        return header_id
    for previous in reversed(response.history):
        header_id = _request_id(previous.headers)
        if header_id:
            return header_id
    if body is None and response.content:
        try:
            body = response.json()
        except ValueError:
            body = None
    value = body.get("request_id") if isinstance(body, dict) else None
    return value if isinstance(value, str) else None


def _replayable(method: str, headers: Mapping[str, str] | None) -> bool:
    """Whether sending a request again cannot act twice: its method, or its key."""
    return method.upper() in _IDEMPOTENT_METHODS or any(
        name.lower() == "idempotency-key" for name in headers or {}
    )


def _should_retry(status: int, replayable: bool) -> bool:
    return status == 429 or (replayable and (status in _RETRY_STATUSES or status >= 500))


def _retry_delay(response: httpx.Response | None, attempt: int) -> float:
    if response is not None:
        value = response.headers.get("retry-after")
        if value:
            try:
                return min(max(float(value), 0.0), 60.0)
            except ValueError:
                try:
                    parsed = cast(datetime | None, email.utils.parsedate_to_datetime(value))
                except (TypeError, ValueError):
                    parsed = None
                if parsed is not None:
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    return min(max((parsed - datetime.now(timezone.utc)).total_seconds(), 0), 60)
    return cast(float, min(0.5 * (2**attempt), 8.0) * (0.75 + random.random() * 0.5))


def _error_from_response(response: httpx.Response) -> APIStatusError:
    try:
        body: Any = response.json()
    except ValueError:
        body = response.text
    request_id = _response_request_id(response, body)
    problem: dict[str, Any] = body if isinstance(body, dict) else {}
    detail = problem.get("detail")
    fields = detail if isinstance(detail, dict) else problem
    if isinstance(detail, str):
        message = detail
    else:
        message = str(
            fields.get("message")
            or fields.get("title")
            or response.reason_phrase
            or f"HTTP {response.status_code}"
        )
    code = fields.get("code")
    classes: dict[int, type[APIStatusError]] = {
        400: BadRequestError,
        401: AuthenticationError,
        403: PermissionDeniedError,
        404: NotFoundError,
        409: ConflictError,
        422: UnprocessableEntityError,
        429: RateLimitError,
    }
    error_class = classes.get(
        response.status_code,
        InternalServerError if response.status_code >= 500 else APIStatusError,
    )
    issues = problem.get("issues")
    return error_class(
        message,
        status_code=response.status_code,
        request_id=request_id,
        code=code if isinstance(code, str) else None,
        body=body,
        headers=response.headers,
        issues=issues if isinstance(issues, list) else [],
    )


def _raw(response: httpx.Response) -> RawResponse[Any]:
    return RawResponse(
        status_code=response.status_code,
        headers=response.headers,
        content=response.content,
        request_id=_response_request_id(response),
    )


class AIInbx(Resources):
    """Synchronous AI Inbx API client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
        default_headers: Mapping[str, str] | None = None,
        **shared: Unpack[SharedHeaders],
    ) -> None:
        api_key = api_key or os.getenv("AI_INBX_API_KEY")
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required; pass it explicitly or set AI_INBX_API_KEY")
        if not 0 <= max_retries <= 5:
            raise ValueError("max_retries must be between 0 and 5")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": f"aiinbx-python/{__version__}",
            **(default_headers or {}),
            **shared_headers(shared),
        }
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(headers=headers)
        if http_client is not None:
            self._http.headers.update(headers)
        self.last_request_id: str | None = None
        Resources.__init__(self, self)
        self.webhooks = Webhooks()

    @property
    def with_raw_response(self) -> RawResources:
        """The same resources, each call answering with a :class:`RawResponse`."""
        return RawResources(self)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        raw: bool = False,
        binary: bool = False,
    ) -> Any:
        replayable = _replayable(method, headers)
        response: httpx.Response | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self._http.request(
                    method,
                    f"{self.base_url}{path}",
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    json=json,
                    headers=headers,
                    timeout=self.timeout if timeout is None else timeout,
                    follow_redirects=True,
                )
            except httpx.TimeoutException as exc:
                if not replayable or attempt >= self.max_retries:
                    raise APITimeoutError("Request timed out") from exc
                time.sleep(_retry_delay(None, attempt))
                continue
            except httpx.RequestError as exc:
                if not replayable or attempt >= self.max_retries:
                    raise APIConnectionError("Could not connect to the AI Inbx API") from exc
                time.sleep(_retry_delay(None, attempt))
                continue
            if _should_retry(response.status_code, replayable) and attempt < self.max_retries:
                time.sleep(_retry_delay(response, attempt))
                continue
            break
        assert response is not None
        self.last_request_id = _response_request_id(response)
        if not response.is_success:
            raise _error_from_response(response)
        if raw:
            return _raw(response)
        if binary:
            return response.content
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> AIInbx:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncAIInbx(AsyncResources):
    """Asynchronous AI Inbx API client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None,
        default_headers: Mapping[str, str] | None = None,
        **shared: Unpack[SharedHeaders],
    ) -> None:
        api_key = api_key or os.getenv("AI_INBX_API_KEY")
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required; pass it explicitly or set AI_INBX_API_KEY")
        if not 0 <= max_retries <= 5:
            raise ValueError("max_retries must be between 0 and 5")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": f"aiinbx-python/{__version__}",
            **(default_headers or {}),
            **shared_headers(shared),
        }
        self._owns_client = http_client is None
        self._http = http_client or httpx.AsyncClient(headers=headers)
        if http_client is not None:
            self._http.headers.update(headers)
        self.last_request_id: str | None = None
        AsyncResources.__init__(self, self)
        self.webhooks = Webhooks()

    @property
    def with_raw_response(self) -> AsyncRawResources:
        """The same resources, each call answering with a :class:`RawResponse`."""
        return AsyncRawResources(self)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        raw: bool = False,
        binary: bool = False,
    ) -> Any:
        import asyncio

        replayable = _replayable(method, headers)
        response: httpx.Response | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._http.request(
                    method,
                    f"{self.base_url}{path}",
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    json=json,
                    headers=headers,
                    timeout=self.timeout if timeout is None else timeout,
                    follow_redirects=True,
                )
            except httpx.TimeoutException as exc:
                if not replayable or attempt >= self.max_retries:
                    raise APITimeoutError("Request timed out") from exc
                await asyncio.sleep(_retry_delay(None, attempt))
                continue
            except httpx.RequestError as exc:
                if not replayable or attempt >= self.max_retries:
                    raise APIConnectionError("Could not connect to the AI Inbx API") from exc
                await asyncio.sleep(_retry_delay(None, attempt))
                continue
            if _should_retry(response.status_code, replayable) and attempt < self.max_retries:
                await asyncio.sleep(_retry_delay(response, attempt))
                continue
            break
        assert response is not None
        self.last_request_id = _response_request_id(response)
        if not response.is_success:
            raise _error_from_response(response)
        if raw:
            return _raw(response)
        if binary:
            return response.content
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    async def close(self) -> None:
        if self._owns_client:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncAIInbx:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
