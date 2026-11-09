from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import cast

from ._errors import WebhookVerificationError
from .models import WebhookEvent


def verify_webhook(
    payload: bytes | str,
    signature: str,
    secret: str,
    *,
    tolerance: int = 300,
    now: int | None = None,
) -> WebhookEvent:
    """Verify and decode an AI Inbx webhook.

    ``signature`` is the ``AIInbx-Signature`` header, ``t=<unix>,v1=<hex>``.
    ``tolerance`` is the accepted age or clock skew in seconds; 0 accepts only
    the same second.
    """
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    body = payload.encode() if isinstance(payload, str) else payload
    parsed_timestamp: str | None = None
    signatures: list[str] = []
    for part in signature.split(","):
        key, _, value = part.strip().partition("=")
        if key == "t":
            parsed_timestamp = value
        elif key == "v1":
            signatures.append(value)
    if parsed_timestamp is None or not signatures:
        raise WebhookVerificationError("Missing webhook timestamp or v1 signature")
    try:
        timestamp_int = int(parsed_timestamp)
    except ValueError as exc:
        raise WebhookVerificationError("Invalid webhook timestamp") from exc
    current = int(time.time()) if now is None else now
    if abs(current - timestamp_int) > tolerance:
        raise WebhookVerificationError("Webhook timestamp is outside the replay window")
    signed = parsed_timestamp.encode() + b"." + body
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, candidate) for candidate in signatures):
        raise WebhookVerificationError("Webhook signature does not match")
    try:
        decoded = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WebhookVerificationError("Webhook payload is not valid JSON") from exc
    if not isinstance(decoded, dict):
        raise WebhookVerificationError("Webhook payload must be a JSON object")
    return cast(WebhookEvent, decoded)


class Webhooks:
    verify = staticmethod(verify_webhook)
