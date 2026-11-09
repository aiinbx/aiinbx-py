from __future__ import annotations

import hashlib
import hmac

import pytest

from aiinbx import WebhookVerificationError, verify_webhook


def signature(payload: bytes, timestamp: int, secret: str) -> str:
    digest = hmac.new(
        secret.encode(), f"{timestamp}.".encode() + payload, hashlib.sha256
    ).hexdigest()
    return f"t={timestamp},v1={digest}"


def test_verifies_signature_and_decodes_payload() -> None:
    payload = b'{"id":"evt_1","type":"email.sent"}'
    event = verify_webhook(
        payload, signature(payload, 1_000, "whsec_test"), "whsec_test", now=1_100
    )
    assert event["id"] == "evt_1"
    assert event["type"] == "email.sent"


def test_rejects_replay_and_tampering() -> None:
    payload = b'{"id":"evt_1"}'
    signed = signature(payload, 1_000, "whsec_test")
    with pytest.raises(WebhookVerificationError, match="replay window"):
        verify_webhook(payload, signed, "whsec_test", now=2_000)
    with pytest.raises(WebhookVerificationError, match="does not match"):
        verify_webhook(b'{"id":"tampered"}', signed, "whsec_test", now=1_000)


def test_tolerance_zero_is_the_same_second_and_cannot_go_negative() -> None:
    payload = b'{"id":"evt_1"}'
    signed = signature(payload, 1_000, "whsec_test")
    assert verify_webhook(payload, signed, "whsec_test", tolerance=0, now=1_000)
    with pytest.raises(WebhookVerificationError, match="replay window"):
        verify_webhook(payload, signed, "whsec_test", tolerance=0, now=1_001)
    with pytest.raises(ValueError, match="non-negative"):
        verify_webhook(payload, signed, "whsec_test", tolerance=-1, now=1_000)


def test_rejects_a_bare_digest() -> None:
    payload = b'{"id":"evt_1"}'
    digest = signature(payload, 1_000, "whsec_test").split("v1=")[1]
    with pytest.raises(WebhookVerificationError, match="Missing"):
        verify_webhook(payload, digest, "whsec_test", now=1_000)
