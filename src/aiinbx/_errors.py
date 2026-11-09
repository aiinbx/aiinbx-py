from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import ProblemIssuesItem


class AIInbxError(Exception):
    """Base class for all SDK errors."""


class APIConnectionError(AIInbxError):
    """The API could not be reached after retrying."""


class APITimeoutError(APIConnectionError):
    """The request exceeded its configured timeout."""


class APIStatusError(AIInbxError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        request_id: str | None,
        code: str | None = None,
        body: Any,
        headers: Mapping[str, str],
        issues: list[ProblemIssuesItem] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        #: Stable machine-readable error code from the problem body, such as ``not_found``.
        self.code = code
        self.body = body
        self.headers = headers
        #: What a request that failed validation got wrong, field by field.
        self.issues = issues or []


class BadRequestError(APIStatusError):
    pass


class AuthenticationError(APIStatusError):
    pass


class PermissionDeniedError(APIStatusError):
    pass


class NotFoundError(APIStatusError):
    pass


class ConflictError(APIStatusError):
    pass


class UnprocessableEntityError(APIStatusError):
    pass


class RateLimitError(APIStatusError):
    pass


class InternalServerError(APIStatusError):
    pass


class WebhookVerificationError(AIInbxError):
    """A webhook signature is invalid, malformed, or outside the replay window."""
