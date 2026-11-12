# AI Inbx Python SDK

[Website](https://aiinbx.com) · [Documentation](https://docs.aiinbx.com)

The official typed Python client for AI Inbx API v2. It supports synchronous and
asynchronous applications, bounded retries, per-request timeouts, raw responses,
idempotency keys, and signed webhook verification.

```bash
pip install aiinbx
```

## Send an email

```python
from aiinbx import AIInbx

with AIInbx() as client:  # reads AI_INBX_API_KEY
    email = client.emails.send(
        {
            "from_": {"name": "AI Inbx", "address": "hello@example.com"},
            "to": ["ada@example.com"],
            "subject": "Hello",
            "text": "Sent with AI Inbx",
        },
        idempotency_key="welcome-ada-v1",
    )
    print(email["id"])
```

The default base URL is `https://api.aiinbx.com/api/v2`. Use `base_url=` to point
the client at a local or self-hosted API. Requests time out after 60 seconds. The
client retries a 429 up to two times always, and network failures, HTTP 408 and 5xx
when a retry cannot act twice — a `GET`, `PUT` or `DELETE`, or a send, reply or
forward with an `idempotency_key` — honoring `Retry-After`. It never retries a 409
or other 4xx.

## Async

```python
from aiinbx import AsyncAIInbx

async with AsyncAIInbx() as client:
    page = await client.threads.list(limit=20)
```

`AsyncAIInbx` mirrors `AIInbx` method for method. Each API resource is an
attribute of the client — `client.emails`, `client.webhook_endpoints`,
`client.pacing_rules` — and every endpoint page in the
[API reference](https://docs.aiinbx.com/api) shows its Python call.

Every operation takes its request body as one dictionary — a `TypedDict` from
`aiinbx.models`, named after the API's schema (`SendEmailRequest`,
`UpdateDomainRequest`, …) — and its query filters as keyword arguments. The
one spelling difference from the wire is `from_`, since `from` is a Python
keyword; the SDK sends it as `from`. Resources, models and these method
signatures are generated from the API contract, so a change to the API is a
change here on the next release.

## Reply and pagination

Replies infer the sender, recipients, subject, and RFC reply headers from the
thread. Supply only the content for the common case:

```python
reply = client.threads.reply(
    "thr_123",
    {"text": "Sounds good — see you Thursday."},
    idempotency_key="reply-thr-123-v1",
)

# `iter()` follows cursors lazily. Async resources support `async for`.
for email in client.emails.iter(direction="inbound"):
    print(email["subject"])

async for message in async_client.threads.iter_messages("thr_123"):
    print(message["snippet"])
```

Sends, replies and forwards take an `idempotency_key`; every call takes a
`timeout` and works under `with_raw_response`.

## Spaces

A space groups a customer's domains, mailboxes, assigned addresses and mail.
Pass `space_id` when creating a domain, mailbox, suppression or pacing rule, or
when assigning a single address; emails and threads inherit the space of the
address they went through when it is assigned to one, else of its domain or
mailbox. Lists of those
take a `space=` filter: pass a space ID for that space, `"none"` for only the
workspace's own resources (`space_id` of `None`), or omit it for both the
workspace and all spaces. API keys and webhook endpoints belong to the
workspace: one key reaches every space, and one endpoint receives every space's
events, each stamped with its `space_id`. Spaces are optional — a workspace
that never creates one sees `space_id` of `None` everywhere.

`external_id` is your own id for the customer — unique per workspace, so a
second create for the same customer fails with `409 external_id_taken` — and
`spaces.list(external_id=...)` finds the space by it.

```python
space = client.spaces.create({"name": "Acme", "external_id": "cus_8812"})
# Later, from your side of the map:
same = client.spaces.list(external_id="cus_8812")["data"][0]
# One label under a wildcard you own (`*.mail.example.com`) is a subdomain: no DNS to publish.
client.domains.create({"name": "acme.mail.example.com", "space_id": space["id"]})
client.emails.send(
    {
        "from_": "Acme <hello@acme.mail.example.com>",
        "to": ["ada@example.com"],
        "subject": "Welcome",
        "text": "Sent from Acme's own subdomain.",
    }
)
# Or one address of a verified domain you already have, in the customer's space: no DNS.
client.addresses.assign({"address": "anna@agents.example.com", "space_id": space["id"]})
assigned = client.addresses.list(space=space["id"])["data"]
client.addresses.remove("anna@agents.example.com")  # back in its domain's space
```

Use the customer's own domain when they bring one, a subdomain when each
customer needs a name of their own or any number of addresses, and an assigned
address when each customer — or each agent — has one or a few addresses on a
domain you already have.

When several addresses of one space write to the same contacts,
`thread_across_addresses` lets mail without reply headers join any thread of
the space, not only one its address takes part in. It starts off; real replies
always join their thread. The workspace has the same switch for mail outside
spaces.

```python
client.spaces.update(space["id"], {"thread_across_addresses": True})
client.workspaces.update({"thread_across_addresses": True})
```

## Raw responses and request IDs

```python
response = client.with_raw_response.emails.retrieve("eml_123")
print(response.status_code, response.request_id)
email = response.json()

# The most recently completed response is also exposed on the client.
print(client.last_request_id)
```

Non-success responses raise typed subclasses of `APIStatusError`. These include
`status_code`, `request_id`, response `headers`, and the decoded `body`.

## Verify webhooks

Always pass the unmodified request body. The verifier signs
`<unix_timestamp>.<payload>` with HMAC-SHA256 and rejects payloads older than five
minutes by default.

```python
event = client.webhooks.verify(
    request_body,
    request.headers["AIInbx-Signature"],
    webhook_secret,
)

# `event` is the `aiinbx.WebhookEvent` union, generated from the API contract.
# Type checkers narrow `data` from the event type.
if event["type"] == "email.bounced":
    for recipient in event["data"]["recipients"]:
        print(recipient)
```

A bad signature, a malformed header, or a timestamp outside the window raises
`WebhookVerificationError`. Override the replay window with `tolerance=` (seconds;
`0` accepts only the same second) only when necessary.

## Contributing

The resources, models and method signatures of this SDK are generated from the AI
Inbx API contract. This repository receives the source of every release published
to [PyPI](https://pypi.org/project/aiinbx/), tagged with its version.
[Issues](https://github.com/aiinbx/aiinbx-py/issues) are welcome. Pull requests are
too: an accepted change is ported into the source repository and arrives here with
the next release.
