from __future__ import annotations

import json
import keyword
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Mapping
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar
from urllib.parse import quote

import httpx
from typing_extensions import TypedDict

T = TypeVar("T")

Timeout = float | httpx.Timeout | None


@dataclass(frozen=True)
class RawResponse(Generic[T]):
    status_code: int
    headers: Mapping[str, str]
    content: bytes
    request_id: str | None

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")

    def json(self) -> T:
        parsed: T = json.loads(self.content)
        return parsed


class CursorPage(TypedDict, Generic[T]):
    """One page of a cursor list; ``next_cursor`` is ``None`` on the last."""

    data: list[T]
    next_cursor: str | None


class SyncTransport(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: Timeout = None,
        raw: bool = False,
        binary: bool = False,
    ) -> Any: ...


class AsyncTransport(Protocol):
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: Timeout = None,
        raw: bool = False,
        binary: bool = False,
    ) -> Any: ...


class SyncResource:
    def __init__(self, client: SyncTransport) -> None:
        self._client = client

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        return self._client.request(method, path, **kwargs)


class SyncRawResource(SyncResource):
    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        return self._client.request(method, path, raw=True, **kwargs)


class AsyncResource:
    def __init__(self, client: AsyncTransport) -> None:
        self._client = client

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        return await self._client.request(method, path, **kwargs)


class AsyncRawResource(AsyncResource):
    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        return await self._client.request(method, path, raw=True, **kwargs)


def path_segment(value: str) -> str:
    return quote(value, safe="")


def idempotency_headers(idempotency_key: str | None) -> Mapping[str, str] | None:
    return {"Idempotency-Key": idempotency_key} if idempotency_key else None


def wire(value: Mapping[str, Any]) -> dict[str, Any]:
    """The body as the API spells it: ``from_`` is ``from``, and so on for every keyword."""
    return {
        key[:-1] if key.endswith("_") and keyword.iskeyword(key[:-1]) else key: item
        for key, item in value.items()
    }


def iterate_pages(fetch: Callable[[str | None], CursorPage[T]]) -> Iterator[T]:
    cursor: str | None = None
    seen: set[str] = set()
    while True:
        page = fetch(cursor)
        yield from page["data"]
        cursor = page["next_cursor"]
        if not cursor:
            return
        if cursor in seen:
            raise RuntimeError("API returned the same pagination cursor more than once")
        seen.add(cursor)


async def iterate_pages_async(
    fetch: Callable[[str | None], Awaitable[CursorPage[T]]],
) -> AsyncIterator[T]:
    cursor: str | None = None
    seen: set[str] = set()
    while True:
        page = await fetch(cursor)
        for item in page["data"]:
            yield item
        cursor = page["next_cursor"]
        if not cursor:
            return
        if cursor in seen:
            raise RuntimeError("API returned the same pagination cursor more than once")
        seen.add(cursor)
