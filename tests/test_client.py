from __future__ import annotations

import json

import httpx
import pytest

from aiinbx import (
    AIInbx,
    APIStatusError,
    AsyncAIInbx,
    ConflictError,
    NotFoundError,
    RawResponse,
)


def test_reads_the_conventional_api_key_environment_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_INBX_API_KEY", "environment-key")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer environment-key"
        return httpx.Response(200, json={"data": [], "next_cursor": None})

    client = AIInbx(http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert client.emails.list()["data"] == []


def test_send_auth_idempotency_and_input_alias() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.aiinbx.com/api/v2/emails"
        assert request.headers["authorization"] == "Bearer secret"
        assert request.headers["idempotency-key"] == "send-1"
        assert json.loads(request.content) == {
            "from": "sender@example.com",
            "to": ["recipient@example.com"],
            "subject": "Hi",
            "text": "Hello",
            "thread_id": "thr_00000000000000000000000000000000",
            "unsubscribe": True,
        }
        return httpx.Response(201, json={"id": "email_1", "status": "queued", "created_at": "now"})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = AIInbx(api_key="secret", http_client=http)
    result = client.emails.send(
        {
            "from_": "sender@example.com",
            "to": ["recipient@example.com"],
            "subject": "Hi",
            "text": "Hello",
            "thread_id": "thr_00000000000000000000000000000000",
            "unsubscribe": True,
        },
        idempotency_key="send-1",
    )
    assert result["id"] == "email_1"


def test_thread_reply_sends_body_and_undoes_the_from_alias() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v2/threads/thr_1/reply"
        assert request.headers["idempotency-key"] == "reply-1"
        assert json.loads(request.content) == {
            "text": "Thanks!",
            "reply_all": True,
            "from": "ada@example.com",
        }
        return httpx.Response(201, json={"id": "eml_reply", "status": "queued"})

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    reply = client.threads.reply(
        "thr_1",
        {"text": "Thanks!", "reply_all": True, "from_": "ada@example.com"},
        idempotency_key="reply-1",
    )
    assert reply["id"] == "eml_reply"


def test_thread_forward_sends_recipient_and_note() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v2/threads/thr_1/forward"
        assert request.headers["idempotency-key"] == "forward-1"
        assert json.loads(request.content) == {
            "to": "human@example.com",
            "note": "Over to you.",
            "include_attachments": False,
        }
        return httpx.Response(201, json={"id": "eml_fwd", "status": "queued"})

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    forward = client.threads.forward(
        "thr_1",
        {"to": "human@example.com", "note": "Over to you.", "include_attachments": False},
        idempotency_key="forward-1",
    )
    assert forward["id"] == "eml_fwd"



def test_thread_reply_preserves_raw_response_mode() -> None:
    client = AIInbx(
        api_key="secret",
        http_client=httpx.Client(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(201, json={"id": "eml_reply", "status": "queued"})
            )
        ),
    )
    response = client.with_raw_response.threads.reply("thr_1", {"html": "<p>Thanks</p>"})
    assert isinstance(response, RawResponse)
    assert response.json()["id"] == "eml_reply"



def test_sync_auto_pagination_follows_cursors() -> None:
    cursors: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        cursor = request.url.params.get("cursor")
        cursors.append(cursor)
        if cursor is None:
            return httpx.Response(200, json={"data": [{"id": "eml_1"}], "next_cursor": "two"})
        return httpx.Response(200, json={"data": [{"id": "eml_2"}], "next_cursor": None})

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    assert [email["id"] for email in client.emails.iter(limit=1)] == ["eml_1", "eml_2"]
    assert cursors == [None, "two"]


def test_domain_management_matches_v2_contract() -> None:
    seen: list[tuple[str, str, dict[str, object], dict[str, str]]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else {}
        seen.append((request.method, request.url.path, body, dict(request.url.params)))
        if request.url.path.endswith("/diagnostics"):
            return httpx.Response(200, json={"data": []})
        return httpx.Response(
            200, json={"id": "dom_1", "tracking": {"opens": True, "clicks": False}}
        )

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    client.domains.update("dom_1", {"track_opens": True})
    client.domains.diagnostics("dom_1")
    assert seen[0][2] == {"track_opens": True}
    assert seen[1][1] == "/api/v2/domains/dom_1/diagnostics"


def test_api_keys_mailbox_sync_and_thread_message_pagination() -> None:
    message_cursors: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v2/api-keys" and request.method == "POST":
            assert json.loads(request.content) == {"name": "Deploy", "scope": "sending"}
            return httpx.Response(
                201,
                json={
                    "id": "key_1",
                    "name": "Deploy",
                    "scope": "sending",
                    "prefix": "ai_live_",
                    "key": "ai_live_secret",
                },
            )
        if request.url.path == "/api/v2/api-keys/key_1":
            return httpx.Response(204)
        if request.url.path == "/api/v2/mailboxes/mbx_1/sync":
            return httpx.Response(202, json={"status": "queued"})
        if request.url.path == "/api/v2/threads/thr_1":
            cursor = request.url.params.get("message_cursor")
            message_cursors.append(cursor)
            if cursor is None:
                return httpx.Response(
                    200,
                    json={
                        "id": "thr_1",
                        "messages": [{"id": "eml_1"}],
                        "messages_next_cursor": "two",
                    },
                )
            return httpx.Response(
                200,
                json={
                    "id": "thr_1",
                    "messages": [{"id": "eml_2"}],
                    "messages_next_cursor": None,
                },
            )
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    created = client.api_keys.create({"name": "Deploy", "scope": "sending"})
    assert created["key"] == "ai_live_secret"
    client.api_keys.delete("key_1")
    assert client.mailboxes.sync("mbx_1")["status"] == "queued"
    assert [message["id"] for message in client.threads.iter_messages("thr_1")] == [
        "eml_1",
        "eml_2",
    ]
    assert message_cursors == [None, "two"]


def test_spaces_crud_filter_and_space_id_on_create() -> None:
    seen: list[tuple[str, str, dict[str, object], dict[str, str]]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else {}
        seen.append((request.method, request.url.path, body, dict(request.url.params)))
        if request.method == "DELETE":
            return httpx.Response(204)
        if request.method == "GET" and request.url.path in {
            "/api/v2/spaces",
            "/api/v2/domains",
            "/api/v2/addresses",
        }:
            return httpx.Response(200, json={"data": [{"id": "spc_1"}], "next_cursor": None})
        return httpx.Response(
            201, json={"id": "spc_1", "name": "Acme", "created_at": "now", "space_id": "spc_1"}
        )

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    created = client.spaces.create({"name": "Acme", "external_id": "cus_1"})
    assert created["name"] == "Acme"
    assert [space["id"] for space in client.spaces.iter()] == ["spc_1"]
    client.spaces.retrieve("spc_1")
    client.spaces.update(
        "spc_1", {"name": "Acme Inc", "external_id": None, "thread_across_addresses": True}
    )
    client.spaces.delete("spc_1")
    client.domains.list(space="spc_1")
    client.domains.create({"name": "acme.example.com", "space_id": "spc_1"})
    client.addresses.assign({"address": "anna@agents.example.com", "space_id": "spc_1"})
    client.addresses.list(address="anna@agents.example.com")
    client.addresses.remove("anna+orders@agents.example.com")
    assert [(method, path) for method, path, _, _ in seen] == [
        ("POST", "/api/v2/spaces"),
        ("GET", "/api/v2/spaces"),
        ("GET", "/api/v2/spaces/spc_1"),
        ("PATCH", "/api/v2/spaces/spc_1"),
        ("DELETE", "/api/v2/spaces/spc_1"),
        ("GET", "/api/v2/domains"),
        ("POST", "/api/v2/domains"),
        ("POST", "/api/v2/addresses"),
        ("GET", "/api/v2/addresses"),
        ("DELETE", "/api/v2/addresses/anna+orders@agents.example.com"),
    ]
    assert seen[0][2] == {"name": "Acme", "external_id": "cus_1"}
    assert seen[3][2] == {
        "name": "Acme Inc",
        "external_id": None,
        "thread_across_addresses": True,
    }
    assert seen[5][3] == {"space": "spc_1"}
    assert seen[6][2] == {"name": "acme.example.com", "space_id": "spc_1"}
    assert seen[7][2] == {"address": "anna@agents.example.com", "space_id": "spc_1"}
    assert seen[8][3] == {"address": "anna@agents.example.com"}


def test_retrieve_email_expands_attachment_content() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v2/emails/eml_1"
        assert request.url.params.get_list("include") == ["attachment_content"]
        return httpx.Response(200, json={"id": "eml_1"})

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    assert client.emails.retrieve("eml_1", include=["attachment_content"])["id"] == "eml_1"


def test_raw_resources_mirror_every_namespace() -> None:
    client = AIInbx(
        api_key="secret",
        http_client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    200, json={"spread": 20}, headers={"X-Request-ID": "req_spread"}
                )
            )
        ),
    )
    raw = client.with_raw_response
    for name in ("spaces", "emails", "threads", "webhook_endpoints", "pacing", "attachments"):
        assert hasattr(raw, name)
    response = raw.pacing_rules.retrieve_spread()
    assert isinstance(response, RawResponse)
    assert response.request_id == "req_spread"
    assert response.json()["spread"] == 20
    assert client.pacing_rules.retrieve_spread()["spread"] == 20


def test_retries_retry_after_and_exposes_request_id() -> None:
    attempts = 0

    def handler(_: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(
            200,
            json={"id": "email_1", "status": "sent", "created_at": "now"},
            headers={"X-Request-ID": "req_123"},
        )

    client = AIInbx(
        api_key="secret",
        max_retries=1,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    result = client.emails.retrieve("email_1")
    assert result["status"] == "sent"
    assert attempts == 2
    assert client.last_request_id == "req_123"


def test_status_error_contains_problem_and_request_id() -> None:
    transport = httpx.MockTransport(
        lambda _: httpx.Response(
            404,
            json={"type": "about:blank", "title": "Not found", "detail": "No email"},
            headers={"X-Request-ID": "req_missing"},
        )
    )
    client = AIInbx(api_key="secret", max_retries=0, http_client=httpx.Client(transport=transport))
    with pytest.raises(NotFoundError) as caught:
        client.emails.retrieve("missing")
    assert caught.value.status_code == 404
    assert caught.value.request_id == "req_missing"
    assert caught.value.body["title"] == "Not found"


def test_problem_request_id_falls_back_to_rfc_9457_body() -> None:
    transport = httpx.MockTransport(
        lambda _: httpx.Response(
            404,
            json={
                "type": "about:blank",
                "title": "Not found",
                "status": 404,
                "detail": "No email",
                "code": "not_found",
                "request_id": "req_from_body",
            },
        )
    )
    client = AIInbx(api_key="secret", max_retries=0, http_client=httpx.Client(transport=transport))
    with pytest.raises(NotFoundError) as caught:
        client.emails.retrieve("missing")
    assert caught.value.request_id == "req_from_body"


def test_binary_endpoint_error_carries_problem_code() -> None:
    transport = httpx.MockTransport(
        lambda _: httpx.Response(
            404,
            json={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": "No prepared text: preparation is failed",
                "code": "not_prepared",
            },
        )
    )
    client = AIInbx(api_key="secret", max_retries=0, http_client=httpx.Client(transport=transport))
    with pytest.raises(NotFoundError) as caught:
        client.attachments.content("att_1")
    assert caught.value.code == "not_prepared"
    assert str(caught.value) == "No prepared text: preparation is failed"


def test_raw_response_and_binary_content() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/content"):
            return httpx.Response(
                200, content=b"attachment", headers={"Content-Type": "text/plain"}
            )
        return httpx.Response(200, json={"id": "email_1"}, headers={"X-Request-ID": "req_raw"})

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    raw = client.with_raw_response.emails.retrieve("email_1")
    assert isinstance(raw, RawResponse)
    assert raw.request_id == "req_raw"
    assert raw.json()["id"] == "email_1"
    assert client.attachments.content("att_1") == "attachment"


def test_management_bodies_and_query_names_match_v2_contract() -> None:
    seen: list[tuple[str, str, dict[str, object]]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else {}
        seen.append((request.method, request.url.path, body))
        if request.url.path == "/api/v2/emails":
            assert request.url.params["direction"] == "outbound"
            assert "mailbox_id" not in request.url.params
        if request.method == "DELETE":
            return httpx.Response(204)
        return httpx.Response(200, json={"data": [], "spread": 20})

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    client.emails.list(direction="outbound")
    client.mailboxes.connect(
        {
            "provider": "google",
            "return_to": "https://example.com/done",
            "app_id": "app_00000000000000000000000000000000",
            "backfill_days": 14,
        }
    )
    client.webhook_endpoints.rotate_secret("wh_1", {"grace_seconds": 60})
    client.suppressions.add(
        {"addresses": ["ada@example.com"], "key": "marketing", "scope": "optional"}
    )
    client.pacing_rules.update_spread({"spread": 20})
    client.pacing.release({"email_ids": ["eml_1", "eml_2"], "count_toward_limits": False})
    assert seen[1][2] == {
        "provider": "google",
        "return_to": "https://example.com/done",
        "app_id": "app_00000000000000000000000000000000",
        "backfill_days": 14,
    }
    assert seen[2][2] == {"grace_seconds": 60}
    assert seen[3][2]["addresses"] == ["ada@example.com"]
    assert seen[4] == ("PATCH", "/api/v2/pacing-rules/spread", {"spread": 20})
    assert seen[5][2] == {"email_ids": ["eml_1", "eml_2"], "count_toward_limits": False}


def test_attachments_follow_redirects_and_return_bytes_and_text() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "api.aiinbx.com":
            suffix = "prepared" if request.url.path.endswith("/content") else "original"
            return httpx.Response(307, headers={"Location": f"https://storage.example/{suffix}"})
        if request.url.path == "/prepared":
            return httpx.Response(200, content=b"prepared text")
        return httpx.Response(200, content=b"\x00\x01binary")

    client = AIInbx(
        api_key="secret", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    assert client.attachments.download("att_1") == b"\x00\x01binary"
    assert client.attachments.content("att_1") == "prepared text"


def test_no_content_delete_returns_none() -> None:
    client = AIInbx(
        api_key="secret",
        http_client=httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(204))),
    )
    client.domains.delete("dom_1")



@pytest.mark.asyncio
async def test_async_client_has_resource_parity() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v2/threads/thread_1"
        return httpx.Response(
            200, json={"id": "thread_1", "created_at": "now", "updated_at": "now"}
        )

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncAIInbx(api_key="secret", http_client=http)
    thread = await client.threads.retrieve("thread_1")
    assert thread["id"] == "thread_1"
    await http.aclose()


@pytest.mark.asyncio
async def test_async_spaces_and_space_filter_parity() -> None:
    seen: list[tuple[str, str, dict[str, str]]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.method, request.url.path, dict(request.url.params)))
        if request.method == "POST":
            assert json.loads(request.content) == {"name": "Acme"}
            return httpx.Response(201, json={"id": "spc_1", "name": "Acme", "created_at": "now"})
        return httpx.Response(200, json={"data": [{"id": "eml_1"}], "next_cursor": None})

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncAIInbx(api_key="secret", http_client=http)
    space = await client.spaces.create({"name": "Acme"})
    ids = [email["id"] async for email in client.emails.iter(space=space["id"])]
    assert ids == ["eml_1"]
    assert seen == [
        ("POST", "/api/v2/spaces", {}),
        ("GET", "/api/v2/emails", {"space": "spc_1"}),
    ]
    await http.aclose()


@pytest.mark.asyncio
async def test_async_pacing_release_uses_v2_body() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v2/pacing-queue/release"
        assert json.loads(request.content) == {
            "email_ids": ["eml_1", "eml_2"],
            "count_toward_limits": False,
        }
        return httpx.Response(200, json={"data": ["eml_1", "eml_2"]})

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncAIInbx(api_key="secret", http_client=http)
    result = await client.pacing.release(
        {"email_ids": ["eml_1", "eml_2"], "count_toward_limits": False}
    )
    assert result["data"] == ["eml_1", "eml_2"]
    await http.aclose()


@pytest.mark.asyncio
async def test_async_reply_and_auto_pagination_parity() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/reply"):
            assert json.loads(request.content) == {"text": "Hello"}
            return httpx.Response(201, json={"id": "eml_reply", "status": "queued"})
        cursor = request.url.params.get("cursor")
        if cursor is None:
            return httpx.Response(200, json={"data": [{"id": "thr_1"}], "next_cursor": "two"})
        return httpx.Response(200, json={"data": [{"id": "thr_2"}], "next_cursor": None})

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncAIInbx(api_key="secret", http_client=http)
    reply = await client.threads.reply("thr_1", {"text": "Hello"})
    assert reply["id"] == "eml_reply"
    ids = [thread["id"] async for thread in client.threads.iter(limit=1)]
    assert ids == ["thr_1", "thr_2"]
    await http.aclose()


def test_retries_a_send_only_with_an_idempotency_key_or_on_429() -> None:
    def attempts_for(status: int, idempotency_key: str | None = None) -> int:
        attempts = 0

        def handler(_: httpx.Request) -> httpx.Response:
            nonlocal attempts
            attempts += 1
            return httpx.Response(status, headers={"Retry-After": "0"}, json={})

        client = AIInbx(
            api_key="secret",
            max_retries=1,
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )
        with pytest.raises(APIStatusError):
            client.threads.reply("thr_1", {"text": "Hi"}, idempotency_key=idempotency_key)
        return attempts

    assert attempts_for(500) == 1
    assert attempts_for(500, "once") == 2
    assert attempts_for(429) == 2
    assert attempts_for(409, "once") == 1


def test_never_retries_a_conflict() -> None:
    attempts = 0

    def handler(_: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(409, json={"code": "external_id_taken"})

    client = AIInbx(
        api_key="secret",
        max_retries=2,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    with pytest.raises(ConflictError):
        client.emails.retrieve("email_1")
    assert attempts == 1


def test_status_error_carries_problem_issues() -> None:
    transport = httpx.MockTransport(
        lambda _: httpx.Response(
            422,
            json={
                "code": "invalid_request",
                "detail": "Request body is invalid",
                "issues": [{"path": "to", "message": "Required"}],
            },
        )
    )
    client = AIInbx(api_key="secret", http_client=httpx.Client(transport=transport))
    with pytest.raises(APIStatusError) as caught:
        client.domains.create({"name": ""})
    assert caught.value.issues == [{"path": "to", "message": "Required"}]
