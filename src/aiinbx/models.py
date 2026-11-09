# Generated from @workspace/api-contract by `bun run sdk:generate`. Do not edit.
from __future__ import annotations

from typing import Any, Literal

from typing_extensions import NotRequired, TypedDict

from ._base import CursorPage

ApiKeyScope = Literal["full", "sending", "read"]


MailRegion = Literal["eu-central-1", "us-east-1"]


MailboxProvider = Literal["google", "microsoft"]


MailboxState = Literal["active", "needs_reauth", "disconnected"]


EmailDirection = Literal["inbound", "outbound"]


EmailStatus = Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"]


EmailCategory = Literal["human", "out_of_office", "auto_reply", "bounce", "verification", "transactional", "notification", "marketing", "spam"]


class EmailAddress(TypedDict):
    name: NotRequired[str | None]
    address: str


class EmailHeader(TypedDict):
    name: str
    value: str


class EmailDraft(TypedDict):
    """Set on an email written as a draft — also after it is sent, so a sent email says whether a
    person approved and changed it.
    """

    drafted_at: str
    edited_at: str | None
    """When its content last changed before it was sent. Null when it went as written."""
    review_url: str | None
    """Where a person reviews, edits and sends it in the console."""


class BodySegment(TypedDict):
    kind: Literal["written", "quoted", "signature"]
    text: str


class AttachmentPreparation(TypedDict):
    status: Literal["ready", "partial", "unsupported", "failed"]
    format: Literal["markdown", "text"] | None
    pages: int | None
    warnings: list[str]
    content_url: str | None
    """Signed URL for the prepared text, good until the attachment's `expires_at`. Opens without the
    API key — and only without it: storage answers a request that carries an `Authorization`
    header with 400. Null when there is no prepared text.
    """
    text: NotRequired[str | None]


class Attachment(TypedDict):
    id: str
    filename: str
    content_type: str
    size: int
    cid: str | None
    download_url: str | None
    """Signed URL for the original bytes, good until `expires_at`. Opens without the API key, so
    treat it as a secret — and do not send the key to it: storage answers a request that carries
    an `Authorization` header with 400. To keep a reference, store the attachment `id` and call
    `GET /attachments/{id}`. Null when the bytes are gone.
    """
    expires_at: str | None
    """When `download_url` and `preparation.content_url` stop working — an hour after the response.
    Read the email again, or call the download endpoint with the attachment ID, for fresh ones.
    """
    preparation: AttachmentPreparation | None


class DeliveryEvent(TypedDict):
    id: str
    type: Literal["drafted", "edited", "scheduled", "canceled", "discarded", "queued", "replayed", "sent", "delivered", "deferred", "bounced", "complained", "rejected", "failed"]
    """What happened. `rejected`: the mail provider refused the message outright — a virus, say —
    and nothing was sent; `detail` says why. The email then fails, as on `failed`.
    """
    at: str
    recipient: str | None
    detail: str | None


class Engagement(TypedDict):
    kind: Literal["open", "click"]
    at: str
    url: str | None
    user_agent: str | None
    bot: bool
    """True when a proxy, security scanner or script made the hit rather than the recipient."""
    bot_reason: Literal["privacy_proxy", "script", "known_bot", "stale_browser", "too_fast"] | None
    """Why: `privacy_proxy` is Apple Mail Privacy Protection fetching on arrival, `script` an HTTP
    library, `known_bot` a scanner or link expander that names itself, `stale_browser` a browser
    build nobody runs any more, `too_fast` within seconds of delivery, sooner than a person could
    act. Null when `bot` is false. More reasons may be added; treat one you do not know as a bot.
    """


class PacingHoldReady(TypedDict):
    kind: Literal["ready"]


class PacingHoldHours(TypedDict):
    kind: Literal["hours"]
    rule_id: str


class PacingHoldLimit(TypedDict):
    kind: Literal["limit"]
    rule_id: str


PacingHold = PacingHoldReady | PacingHoldHours | PacingHoldLimit


class EmailPacing(TypedDict):
    held_by: PacingHold
    estimated_send_at: str | None


class DnsRecord(TypedDict):
    purpose: Literal["SPF", "DKIM", "DMARC", "RETURN_PATH", "INBOUND"]
    type: Literal["MX", "TXT", "CNAME"]
    name: str
    value: str
    ttl: int
    state: Literal["pending", "verified", "missing"]
    last_checked_at: str | None


class DnsFinding(TypedDict):
    id: str
    severity: Literal["breaking", "risk", "tip"]
    when: Literal["adding", "added", "both"]
    purpose: NotRequired[Literal["SPF", "DKIM", "DMARC", "RETURN_PATH", "INBOUND"]]
    title: str
    detail: str
    fix: str
    evidence: list[str]


class DomainTracking(TypedDict):
    opens: bool
    clicks: bool


WebhookEventType = Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]


class WebhookRoutingRule(TypedDict):
    effect: Literal["allow", "block"]
    field: Literal["from", "to", "either"]
    pattern: str


class EventAttachment(TypedDict):
    """An attachment's metadata. Its content is on the email, or in `data.email` for a `full`
    endpoint.
    """

    id: str
    filename: str
    content_type: str
    size: int
    preparation: Literal["ready", "partial", "unsupported", "failed"]


class EmailVerdicts(TypedDict):
    """What the receiving side thought of the message. Null when it did not say: mail that arrived
    through a connected mailbox, and mail you sent — unless it was addressed to a domain of yours
    and came back in.
    """

    spam: str | None
    """`PASS`, `FAIL`, `GRAY` or `PROCESSING_FAILED`. Null when this check was not reported."""
    spf: str | None
    """`PASS`, `FAIL`, `GRAY` or `PROCESSING_FAILED`. Null when this check was not reported."""
    dkim: str | None
    """`PASS`, `FAIL`, `GRAY` or `PROCESSING_FAILED`. Null when this check was not reported."""
    dmarc: str | None
    """`PASS`, `FAIL`, `GRAY` or `PROCESSING_FAILED`. Null when this check was not reported."""


class EmailVerification(TypedDict):
    """On a `verification` email: the code and the link it asks the recipient to use. Null on every
    other category, and when it carries neither.
    """

    code: str | None
    """The one-time code to type in, as the email writes it: `482913`, `482 913`, `G-482913`. Null
    when it gives none.
    """
    link: str | None
    """The link that verifies, confirms, signs in or resets, exactly as the email links it. Null
    when it has none.
    """


class EmailUnavailable(TypedDict):
    """On an `out_of_office` or `auto_reply` email that says its sender cannot be reached: why, the
    day they are back, and who to write to instead. Null otherwise — a ticket acknowledgement, a
    thank-you.
    """

    reason: Literal["absent", "left", "unmonitored"]
    """`absent`: away for now — holiday, leave, travel. `left`: no longer at this address.
    `unmonitored`: nobody reads it. More reasons may be added; treat one you do not know as
    unreachable.
    """
    back_on: str | None
    """The first day the sender is back, when the reply says. A reply away "until" a day is read as
    back the next working day. Null when it names no day, when that day had already passed when
    the reply arrived, and for `left` and `unmonitored`.
    """
    contacts: list[str]
    """Addresses the reply says to write to instead — a colleague, a team inbox. Empty when it names
    none.
    """


FullEmail = TypedDict(
    "FullEmail",
    {
        "id": str,
        "thread_id": str,
        "space_id": str | None,
        "direction": EmailDirection,
        "status": EmailStatus,
        "from": EmailAddress,
        "to": list[str],
        "delivered_to": list[str],
        "cc": list[str],
        "bcc": list[str],
        "reply_to": list[str],
        "subject": str,
        "snippet": str,
        "html": str | None,
        "text": str | None,
        "category": EmailCategory | None,
        "verdicts": EmailVerdicts | None,
        "verification": EmailVerification | None,
        "unavailable": EmailUnavailable | None,
        "suppression_key": str | None,
        "message_id": str,
        "in_reply_to": str | None,
        "idempotency_key": str | None,
        "created_at": str,
        "scheduled_at": str | None,
        "sent_at": str | None,
        "draft": EmailDraft | None,
        "attachments": list[Attachment],
        "stripped_text": str | None,
        "stripped_html": str | None,
        "segments": list[BodySegment],
        "references": list[str],
        "headers": list[EmailHeader],
        "events": list[DeliveryEvent],
        "engagements": list[Engagement],
    },
)


EmailReceivedEventData = TypedDict(
    "EmailReceivedEventData",
    {
        "email_id": str,
        "message_id": str,
        "thread_id": str,
        "domain_id": str | None,
        "mailbox_id": str | None,
        "from": str,
        "to": list[str],
        "subject": str,
        "snippet": str,
        "attachments": NotRequired[list[EventAttachment]],
        "email": NotRequired[FullEmail | None],
        "delivered_to": list[str],
        "category": EmailCategory | None,
        "verdicts": EmailVerdicts | None,
        "verification": EmailVerification | None,
        "unavailable": EmailUnavailable | None,
    },
)


EmailSentEventData = TypedDict(
    "EmailSentEventData",
    {
        "email_id": str,
        "message_id": str,
        "thread_id": str,
        "domain_id": str | None,
        "mailbox_id": str | None,
        "from": str,
        "to": list[str],
        "subject": str,
        "snippet": str,
        "attachments": NotRequired[list[EventAttachment]],
        "email": NotRequired[FullEmail | None],
        "suppression_key": str | None,
    },
)


class EmailDeliveredEventData(TypedDict):
    email_id: str
    """The email, `eml_…`. Retrieve it for bodies and headers."""
    message_id: str
    """The RFC Message-ID, without angle brackets."""
    thread_id: str
    """The conversation it belongs to."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    suppression_key: str | None
    """The suppression list the send named, when it named one."""
    recipients: list[str]
    """Which recipients this event covers: delivery is reported per recipient."""


BounceCause = Literal["bad_address", "mailbox_full", "sender_auth", "blocked", "content", "expired", "routing", "unknown"]
"""Why the mail did not arrive. `bad_address`: the address does not exist or no longer takes mail.
`mailbox_full`: it exists and is over its quota. `sender_auth`: the receiving side would not take
it as from the sending domain — DMARC, SPF or DKIM failed — which is fixed in the domain's DNS
records. `blocked`: refused by the receiving side's policy — a blocklist, the sender's
reputation, a recipient that only takes mail from some senders. `content`: the message itself —
its content, an attachment, its size. `expired`: retried until the provider gave up. `routing`:
no route to the recipient, a loop. `unknown`: none of these could be read from what was said.
More causes may be added; treat one you do not know as `unknown`.
"""


class EmailBounce(TypedDict):
    address: str
    cause: BounceCause
    suppressed: bool
    """True when the address is dead and went on the workspace's `*` suppression list, so the next
    send to it never leaves. Only a hard bounce of a `bad_address`, or one nothing explains, is.
    Not SES refusing the send off its own suppression list: that reports `bad_address` without
    suppressing.
    """


class EmailBouncedEventData(TypedDict):
    email_id: str
    """The email, `eml_…`. Retrieve it for bodies and headers."""
    message_id: str
    """The RFC Message-ID, without angle brackets."""
    thread_id: str
    """The conversation it belongs to."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    suppression_key: str | None
    """The suppression list the send named, when it named one."""
    recipients: list[str]
    """Which recipients bounced: the message did not reach them, and nothing will try again."""
    bounces: NotRequired[list[EmailBounce]]
    """One entry per address in `recipients`, in the same order: why it bounced, and whether it was
    suppressed. Absent from an event recorded before this field existed, which `GET /events` and
    a replay still return as it was.
    """
    permanent: bool
    """True when the provider classed the bounce as hard — it gave up for good, as SES's `Permanent`
    or a 5.x status says. False for a soft one, which the provider also stopped retrying. Not
    whether the address is dead: a hard bounce can be a blocklist or the sender's own DMARC. Read
    `bounces` for that.
    """
    reason: str
    """The provider's classification: `Permanent/General` from SES, the status (`5.1.1`) from a
    delivery report.
    """


class EmailComplainedEventData(TypedDict):
    email_id: str
    """The email, `eml_…`. Retrieve it for bodies and headers."""
    message_id: str
    """The RFC Message-ID, without angle brackets."""
    thread_id: str
    """The conversation it belongs to."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    suppression_key: str | None
    """The suppression list the send named: where the complaint is filed, in the send's space."""
    recipients: list[str]
    """Who complained."""
    reason: str | None
    """The provider's reason, when it gave one."""


SuppressionScope = Literal["all", "optional"]


class EmailUnsubscribedEventData(TypedDict):
    email_id: str
    """The message they opted out from, `eml_…`."""
    message_id: str | None
    """The RFC Message-ID, without angle brackets. Null once the message is gone."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    address: str
    """Who opted out."""
    key: str
    """The suppression list. `*` is the whole workspace's, or the whole space's when the send was
    from one.
    """
    scope: SuppressionScope
    """Whether they blocked everything (`all`) or only optional mail (`optional`)."""
    source: Literal["link", "one_click", "reply"]
    """How: the unsubscribe link, the mail client's one-click header, or a reply that read as an
    opt-out.
    """


class EmailFailedEventData(TypedDict):
    email_id: str
    """The email, `eml_…`. Retrieve it for bodies and headers."""
    message_id: str
    """The RFC Message-ID, without angle brackets."""
    thread_id: str
    """The conversation it belongs to."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    suppression_key: str | None
    """The suppression list the send named, when it named one."""
    reason: str
    """What the provider said: why the message never went out."""


class EmailOpenedEventData(TypedDict):
    email_id: str
    """The email, `eml_…`. Retrieve it for bodies and headers."""
    message_id: str
    """The RFC Message-ID, without angle brackets."""
    thread_id: str
    """The conversation it belongs to."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    suppression_key: str | None
    """The suppression list the send named, when it named one."""
    user_agent: str | None
    """The client that loaded the tracking pixel."""
    bot: bool
    """True when a proxy, security scanner or script made the hit rather than the recipient."""
    bot_reason: Literal["privacy_proxy", "script", "known_bot", "stale_browser", "too_fast"] | None
    """Why: `privacy_proxy` is Apple Mail Privacy Protection fetching on arrival, `script` an HTTP
    library, `known_bot` a scanner or link expander that names itself, `stale_browser` a browser
    build nobody runs any more, `too_fast` within seconds of delivery, sooner than a person could
    act. Null when `bot` is false. More reasons may be added; treat one you do not know as a bot.
    """


class EmailClickedEventData(TypedDict):
    email_id: str
    """The email, `eml_…`. Retrieve it for bodies and headers."""
    message_id: str
    """The RFC Message-ID, without angle brackets."""
    thread_id: str
    """The conversation it belongs to."""
    domain_id: str | None
    """The domain the message went through: received on or sent from. Null when it went through a
    mailbox.
    """
    mailbox_id: str | None
    """The mailbox the message went through: synced from or sent with. Null when it went through a
    domain.
    """
    suppression_key: str | None
    """The suppression list the send named, when it named one."""
    url: str
    """The destination that was clicked."""
    user_agent: str | None
    """The client that followed the link."""
    bot: bool
    """True when a proxy, security scanner or script made the hit rather than the recipient."""
    bot_reason: Literal["privacy_proxy", "script", "known_bot", "stale_browser", "too_fast"] | None
    """Why: `privacy_proxy` is Apple Mail Privacy Protection fetching on arrival, `script` an HTTP
    library, `known_bot` a scanner or link expander that names itself, `stale_browser` a browser
    build nobody runs any more, `too_fast` within seconds of delivery, sooner than a person could
    act. Null when `bot` is false. More reasons may be added; treat one you do not know as a bot.
    """


class ThreadCreatedEventData(TypedDict):
    thread_id: str
    """The new conversation, `thr_…`."""
    subject: str
    """The opening subject."""
    mailbox: str
    """The address on your side."""
    forward_of: str | None
    """Set when a forward opened the thread: the conversation it carries."""


class DomainEventData(TypedDict):
    domain_id: str
    """The domain, `dom_…`."""
    name: str
    """The domain name."""
    region: MailRegion
    """The region it sends and receives in."""


class DomainAtRiskEventData(TypedDict):
    domain_id: str
    """The domain, `dom_…`."""
    name: str
    """The domain name."""
    region: MailRegion
    """The region it sends and receives in."""
    dkim_missing_since: str
    """When the domain's DKIM record was found missing from DNS. The domain keeps sending meanwhile."""
    stops_sending_at: str
    """When the domain is lost if the DKIM record is not restored: 72 hours after
    `dkim_missing_since`. Then `verified_at` goes null and `domain.lost` is sent.
    """


class MailboxConnectedEventData(TypedDict):
    mailbox_id: str
    """The mailbox, `mbx_…`."""
    address: str
    """The mailbox address."""
    provider: MailboxProvider
    """Which provider hosts the mailbox."""
    ref: str | None
    """The mailbox's `ref`: what you put on the connect link or passed to `mailboxes.connect`. How
    you match the mailbox to your user.
    """
    metadata: dict[str, str]
    """Your own key-value pairs, stored and given back as they are. Up to 50 keys; a key is 1–40
    characters, a value up to 500. Written whole: what you send replaces what was there.
    """
    app_id: str | None
    """The OAuth app of yours the mailbox was connected through."""
    reconnected: bool
    """True when this replaced an existing authorization rather than adding a new mailbox."""


class MailboxStateEventData(TypedDict):
    mailbox_id: str
    """The mailbox, `mbx_…`."""
    address: str
    """The mailbox address."""
    provider: MailboxProvider
    """Which provider hosts the mailbox."""
    ref: str | None
    """The mailbox's `ref`: what you put on the connect link or passed to `mailboxes.connect`. How
    you match the mailbox to your user.
    """
    metadata: dict[str, str]
    """Your own key-value pairs, stored and given back as they are. Up to 50 keys; a key is 1–40
    characters, a value up to 500. Written whole: what you send replaces what was there.
    """
    reason: str | None
    """What the provider said, when it said anything."""


class WebhookAttempt(TypedDict):
    id: str
    attempted_at: str
    status_code: int | None
    duration_ms: int
    error: str | None
    response: str | None


DeliveryState = Literal["pending", "delivered", "failed"]


SuppressionReason = Literal["complaint", "bounce", "unsubscribe", "manual"]


class PacingMatch(TypedDict):
    field: Literal["from", "to", "either"]
    pattern: str


class PacingWindow(TypedDict):
    days: list[int]
    """Weekdays the window opens on: 0 = Monday … 6 = Sunday."""
    start_minute: int
    end_minute: int


class PacingJitter(TypedDict):
    open_early_minutes: int
    open_late_minutes: int
    close_early_minutes: int
    close_late_minutes: int


class PacingSchedule(TypedDict):
    timezone: str
    windows: list[PacingWindow]
    jitter: NotRequired[PacingJitter]


class PacingScheduleState(TypedDict):
    timezone: str
    windows: list[PacingWindow]
    jitter: PacingJitter


class PacingLimit(TypedDict):
    scope: Literal["rule", "from_address", "from_domain", "to_address", "to_domain"]
    amount: int
    per_seconds: int


PacingQueueItem = TypedDict(
    "PacingQueueItem",
    {
        "email_id": str,
        "space_id": str | None,
        "from": str,
        "to": list[str],
        "subject": str,
        "queued_at": str,
    },
)


class PacingRuleCount(TypedDict):
    rule_id: str
    matches: int
    held: int


class Inbox(TypedDict):
    """An address of the workspace an OAuth connection acts as, in place of the whole workspace: it
    reads the threads filed under the address or that the address took part in, and sends,
    replies and forwards only as it.
    """

    id: str
    address: str
    """The address it reads and sends as."""
    name: str | None
    """The name its mail goes out under, when one was given."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """


ConnectionMode = Literal["workspace", "inbox"]
"""What the caller acts as: `inbox` for an OAuth connection made an inbox on the consent page, held
to the addresses in each workspace's `inboxes`; `workspace` for one to the whole of its
workspaces, and for an API key.
"""


WorkspaceRole = Literal["owner", "admin", "member"]


MemberRole = Literal["admin", "member"]
"""Owner is never given here: the workspace changes hands by a transfer, in the console."""


class SenderObject(TypedDict):
    name: NotRequired[str]
    address: str


Sender = str | SenderObject


class AttachmentInput(TypedDict):
    filename: str
    content_type: str
    content: str
    cid: NotRequired[str]


class SendPacing(TypedDict):
    """The send's say over pacing: `skip: true` goes past every rule, `count: false` uses up none of
    their limits.
    """

    skip: NotRequired[bool]
    count: NotRequired[bool]


class SendTracking(TypedDict):
    """Overrides the sending domain's tracking settings for this email. Only mail sent from a domain
    is tracked: `true` on a send from a connected mailbox is refused with `tracking_unavailable`.
    """

    opens: NotRequired[bool]
    """Whether opens are tracked on this email. Omit to follow the domain's `tracking.opens`."""
    clicks: NotRequired[bool]
    """Whether links are rewritten to track clicks on this email. Omit to follow the domain's
    `tracking.clicks`.
    """


class CreateSpaceRequest(TypedDict):
    name: str
    """The space's name."""
    external_id: NotRequired[str]
    """Your own id for the customer the space stands for. Unique per workspace."""


class UpdateSpaceRequest(TypedDict):
    name: NotRequired[str]
    """The space's name."""
    external_id: NotRequired[str | None]
    """Null clears it."""


class CreateApiKeyRequest(TypedDict):
    name: str
    """What the key is for, as the console lists it."""
    scope: NotRequired[ApiKeyScope]
    """What the key may do: `read`, `sending`, or `full`. Pick the narrowest that works."""


class SendEmailRequest(TypedDict):
    from_: NotRequired[Sender]
    """The sender, `you@yourdomain.com` or `Name <you@yourdomain.com>`, on a verified domain or a
    connected mailbox. Required, except from a connection made an inbox: left out, it sends as
    its inbox on the thread in `thread_id` — the one mail on the thread last went through, on a
    tie the one the thread is filed under — or as its only one. With several and none of them on
    the thread, it has to be named.
    """
    to: str | list[str]
    """Recipients: one address or a list, at most 100."""
    subject: str
    """The subject line."""
    thread_id: NotRequired[str]
    """Continue this thread: the email answers its latest message, and `In-Reply-To` and
    `References` are written from it.
    """
    in_reply_to: NotRequired[str]
    """The Message-ID this email answers, with or without angle brackets — for a reply to a message
    AI Inbx may never have seen. When it names an email of yours the send joins that thread;
    otherwise it opens one. Not with `thread_id`.
    """
    references: NotRequired[list[str]]
    """The Message-IDs of the conversation so far, oldest first, written as `References`.
    `in_reply_to` is added at the end when it is not already there, and stands alone when this is
    left out. Not with `thread_id`.
    """
    cc: NotRequired[str | list[str]]
    """Cc recipients: one address or a list, at most 100."""
    bcc: NotRequired[str | list[str]]
    """Bcc recipients, hidden from the others: one address or a list, at most 100."""
    reply_to: NotRequired[str | list[str]]
    """Where replies go (Reply-To), when not to the sender: one address or a list, at most 100."""
    attachments: NotRequired[list[AttachmentInput]]
    """Files to attach, at most 20 and 3 MB decoded in total: `filename`, `content_type` and
    `content` in base64, and a `cid` to make one an inline image.
    """
    headers: NotRequired[dict[str, str]]
    """Extra headers to write on the message. `Message-ID`, `In-Reply-To` and `References` are the
    API's to write and are refused.
    """
    suppression_key: NotRequired[str]
    """The suppression list the send is checked against, besides the workspace-wide `*` list."""
    pacing: NotRequired[SendPacing]
    tracking: NotRequired[SendTracking]
    scheduled_at: NotRequired[str]
    """When to send, as an ISO 8601 time, at most 30 days out. On a draft, the time proposed for it."""
    draft: NotRequired[bool]
    """Keep it as a draft for a person to review: nothing is sent until it is sent with `POST
    /emails/{id}/send` or from the console, at `draft.review_url`. A draft uses none of the
    plan's emails until then.
    """
    html: NotRequired[str]
    """The HTML body."""
    text: NotRequired[str]
    """The plain-text body."""
    unsubscribe: NotRequired[bool]
    """Marks the email non-essential: it carries one-click unsubscribe headers, and `optional`
    suppressions apply to it. One recipient only.
    """


class UpdateEmailRequestAttachmentsItemObject(TypedDict):
    id: str
    """An attachment this email has."""


class UpdateEmailRequest(TypedDict):
    to: NotRequired[str | list[str]]
    """Recipients: one address or a list, at most 100."""
    cc: NotRequired[str | list[str]]
    """Cc recipients: one address or a list, at most 100. An empty list clears it."""
    bcc: NotRequired[str | list[str]]
    """Bcc recipients: one address or a list, at most 100. An empty list clears it."""
    reply_to: NotRequired[str | list[str]]
    """Where replies go (Reply-To): one address or a list, at most 100. An empty list clears it."""
    subject: NotRequired[str]
    """The subject line."""
    html: NotRequired[str | None]
    """The HTML body. Null drops it, leaving the text. The text part is not rewritten from it — send
    `text` too to keep the two alike.
    """
    text: NotRequired[str | None]
    """The plain-text body. Null drops it, leaving the HTML."""
    attachments: NotRequired[list[AttachmentInput | UpdateEmailRequestAttachmentsItemObject]]
    """The files it carries from now on: `{ id }` keeps one it has, a new one is given as on send.
    Left out, they stay; an empty list removes them all. New files decode to at most 3 MB per
    request, and all the email carries to at most 7 MB.
    """
    scheduled_at: NotRequired[str]
    """The new send time, at most 30 days out — on a draft, the time proposed for it."""


class SendDraftRequest(TypedDict):
    scheduled_at: NotRequired[str]
    """When to send it, at most 30 days out. Left out, the time proposed on the draft while it is
    ahead, or now.
    """


class ReplyThreadRequest(TypedDict):
    from_: NotRequired[Sender]
    """The sender, `you@yourdomain.com` or `Name <you@yourdomain.com>`. Defaults to the thread's
    own; from a connection made an inbox, to its inbox on the thread — the one mail on the thread
    last went through, on a tie the one the thread is filed under. With several and none of them
    on the thread, it has to be named.
    """
    email_id: NotRequired[str]
    """The email in the thread this answers. Its Reply-To, sender and recipients decide whom the
    reply goes to, and `In-Reply-To` names it — also when a draft or scheduled reply goes out
    later. Defaults to the thread's latest email. Pass the id from `email.received` so mail
    arriving meanwhile cannot change whom you answer.
    """
    to: NotRequired[str | list[str]]
    """Recipients in place of the ones the answered email implies — its Reply-To, else its sender,
    or when that email is yours, whom it went to: one address or a list, at most 100.
    """
    reply_all: NotRequired[bool]
    """Answer everyone on the answered email, as a mail client's Reply all does: its Reply-To (else
    its sender) and its `to` go in `to`, its `cc` in `cc`. With a Reply-To set, the sender is
    left out, as in Gmail. Only the address the reply goes out as, and its mailbox's aliases, are
    left off; colleagues stay. When the email is yours, its `to` and `cc` again. A `cc` given is
    added to the inferred one; a `to` given replaces it.
    """
    subject: NotRequired[str]
    """The subject, in place of `Re:` and the thread's."""
    cc: NotRequired[str | list[str]]
    """Cc recipients: one address or a list, at most 100."""
    bcc: NotRequired[str | list[str]]
    """Bcc recipients, hidden from the others: one address or a list, at most 100."""
    reply_to: NotRequired[str | list[str]]
    """Where replies go (Reply-To), when not to the sender: one address or a list, at most 100."""
    attachments: NotRequired[list[AttachmentInput]]
    """Files to attach, at most 20 and 3 MB decoded in total: `filename`, `content_type` and
    `content` in base64, and a `cid` to make one an inline image.
    """
    headers: NotRequired[dict[str, str]]
    """Extra headers to write on the message. `Message-ID`, `In-Reply-To` and `References` are the
    API's to write and are refused.
    """
    suppression_key: NotRequired[str]
    """The suppression list the send is checked against, besides the workspace-wide `*` list."""
    pacing: NotRequired[SendPacing]
    tracking: NotRequired[SendTracking]
    scheduled_at: NotRequired[str]
    """When to send, as an ISO 8601 time, at most 30 days out. On a draft, the time proposed for it."""
    draft: NotRequired[bool]
    """Keep it as a draft for a person to review: nothing is sent until it is sent with `POST
    /emails/{id}/send` or from the console, at `draft.review_url`. A draft uses none of the
    plan's emails until then.
    """
    html: NotRequired[str]
    """The HTML body."""
    text: NotRequired[str]
    """The plain-text body."""
    unsubscribe: NotRequired[bool]
    """Marks the email non-essential: it carries one-click unsubscribe headers, and `optional`
    suppressions apply to it. One recipient only.
    """


class ForwardThreadRequest(TypedDict):
    from_: NotRequired[Sender]
    """The sender, `you@yourdomain.com` or `Name <you@yourdomain.com>`. Defaults to the thread's
    mailbox; from a connection made an inbox, to its inbox on the thread — the one mail on the
    thread last went through, on a tie the one the thread is filed under. With several and none
    of them on the thread, it has to be named.
    """
    to: str | list[str]
    """Recipients: one address or a list, at most 100."""
    subject: NotRequired[str]
    """The subject. Defaults to `Fwd:` and the thread's."""
    note: NotRequired[str]
    """Text placed above the forwarded conversation."""
    include_attachments: NotRequired[bool]
    """Whether the thread's attachments go along."""
    cc: NotRequired[str | list[str]]
    """Cc recipients: one address or a list, at most 100."""
    bcc: NotRequired[str | list[str]]
    """Bcc recipients, hidden from the others: one address or a list, at most 100."""
    reply_to: NotRequired[str | list[str]]
    """Where replies go (Reply-To), when not to the sender: one address or a list, at most 100."""
    attachments: NotRequired[list[AttachmentInput]]
    """Files to attach, at most 20 and 3 MB decoded in total: `filename`, `content_type` and
    `content` in base64, and a `cid` to make one an inline image.
    """
    headers: NotRequired[dict[str, str]]
    """Extra headers to write on the message. `Message-ID`, `In-Reply-To` and `References` are the
    API's to write and are refused.
    """
    suppression_key: NotRequired[str]
    """The suppression list the send is checked against, besides the workspace-wide `*` list."""
    pacing: NotRequired[SendPacing]
    tracking: NotRequired[SendTracking]
    scheduled_at: NotRequired[str]
    """When to send, as an ISO 8601 time, at most 30 days out. On a draft, the time proposed for it."""
    draft: NotRequired[bool]
    """Keep it as a draft for a person to review: nothing is sent until it is sent with `POST
    /emails/{id}/send` or from the console, at `draft.review_url`. A draft uses none of the
    plan's emails until then.
    """


class CreateDomainRequest(TypedDict):
    name: str
    """A domain, a wildcard (`*.acme.dev`), or one label under a wildcard you own (`hi.acme.dev`) —
    the last is created as a subdomain with no records.
    """
    region: NotRequired[MailRegion]
    """The region the domain's mail is handled in."""
    space_id: NotRequired[str]
    """Which space a created resource goes in. Omitted, the workspace itself."""
    track_opens: NotRequired[bool]
    """Whether opens are tracked on mail sent from the domain."""
    track_clicks: NotRequired[bool]
    """Whether links are rewritten to track clicks on mail sent from the domain."""


class UpdateDomainRequest(TypedDict):
    track_opens: NotRequired[bool]
    """Whether opens are tracked on mail sent from the domain."""
    track_clicks: NotRequired[bool]
    """Whether links are rewritten to track clicks on mail sent from the domain."""
    region: NotRequired[MailRegion]
    """Move a domain that has not verified yet to another region. Its MX and return-path records
    change with it and start over as pending; DKIM does not. `409 region_fixed` once it is
    verified, or on a subdomain.
    """


class ConnectMailboxRequest(TypedDict):
    provider: MailboxProvider
    """`google` for Gmail, `microsoft` for Outlook."""
    app_id: NotRequired[str]
    """Your own OAuth app to connect through, so consent shows your product's name."""
    space_id: NotRequired[str]
    """Which space a created resource goes in. Omitted, the workspace itself."""
    return_to: str
    """Where the person is sent once they have authorized."""
    ref: NotRequired[str]
    """Your own identifier for whoever the mailbox belongs to. Kept on the mailbox and carried on
    every `mailbox.*` event.
    """
    metadata: NotRequired[dict[str, str]]
    """Your own key-value pairs, stored and given back as they are. Up to 50 keys; a key is 1–40
    characters, a value up to 500. Written whole: what you send replaces what was there.
    """
    region: NotRequired[MailRegion]
    """The region the mailbox's mail is handled in."""
    backfill_days: NotRequired[int]
    """Days of existing mail to import, up to 90."""


class CreateOAuthAppRequest(TypedDict):
    provider: MailboxProvider
    """`google` for Gmail, `microsoft` for Outlook."""
    name: str
    """Your product's name, as the consent screen shows it."""
    slug: str
    """The connect URL's name. Unique across all of AI Inbx."""
    client_id: str
    """The OAuth client id, from Google Cloud or Microsoft Entra."""
    client_secret: str
    """The OAuth client secret that goes with the client id."""
    tenant: NotRequired[str]
    """Microsoft only: the Entra tenant, for an app registered to one."""
    pubsub_topic: NotRequired[str]
    """Google only: your Pub/Sub topic, which Gmail publishes mailbox changes to."""
    accent: NotRequired[str]
    """The accent colour of your connect page."""
    tagline: NotRequired[str]
    """A line under your product's name on the connect page."""
    support_email: NotRequired[str]
    """Where people connecting a mailbox can reach you."""
    logo_url: NotRequired[str]
    """Your logo, linked from your own server."""
    return_urls: NotRequired[list[str]]
    """The pages a connect link may return to. Replaced whole on update."""


class UpdateOAuthAppRequest(TypedDict):
    name: NotRequired[str]
    """Your product's name, as the consent screen shows it."""
    client_id: NotRequired[str]
    """The OAuth client id, from Google Cloud or Microsoft Entra."""
    client_secret: NotRequired[str]
    """The OAuth client secret that goes with the client id."""
    tenant: NotRequired[str | None]
    """Microsoft only: the Entra tenant, for an app registered to one. Null clears it."""
    pubsub_topic: NotRequired[str | None]
    """Google only: your Pub/Sub topic, which Gmail publishes mailbox changes to. Null clears it."""
    accent: NotRequired[str | None]
    """The accent colour of your connect page. Null clears it."""
    tagline: NotRequired[str | None]
    """A line under your product's name on the connect page. Null clears it."""
    support_email: NotRequired[str | None]
    """Where people connecting a mailbox can reach you. Null clears it."""
    logo_url: NotRequired[str | None]
    """Your logo, linked from your own server. Null clears it."""
    return_urls: NotRequired[list[str]]
    """The pages a connect link may return to. Replaced whole on update."""


class WebhookEndpointRequest(TypedDict):
    url: str
    """Where deliveries are POSTed."""
    enabled: NotRequired[bool]
    """Whether the endpoint receives deliveries."""
    subscriptions: list[WebhookEventType]
    """The event types to deliver, at least one."""
    routing: NotRequired[list[WebhookRoutingRule]]
    """Rules that narrow delivery by sender or recipient, such as
    `[{"effect":"block","field":"from","pattern":"..."}]`. A matching block wins.
    """
    max_concurrency: NotRequired[int]
    """Deliveries in flight to this endpoint at once."""
    payload: NotRequired[Literal["summary", "full"]]
    """How much of a message `email.received` and `email.sent` carry. `summary` is the addresses,
    subject and snippet; `full` adds `data.email`, the email as `GET
    /emails/{id}?include=attachment_content` returns it, so a handler has no second call to make.
    Every other event is the same either way, and an endpoint whose `format` is `v1` cannot be
    `full`.
    """


class UpdateWebhookEndpointRequest(TypedDict):
    url: NotRequired[str]
    """Where deliveries are POSTed."""
    enabled: NotRequired[bool]
    """Whether the endpoint receives deliveries."""
    subscriptions: NotRequired[list[WebhookEventType]]
    """The event types to deliver, at least one."""
    routing: NotRequired[list[WebhookRoutingRule]]
    """Rules that narrow delivery by sender or recipient, such as
    `[{"effect":"block","field":"from","pattern":"..."}]`. A matching block wins.
    """
    max_concurrency: NotRequired[int]
    """Deliveries in flight to this endpoint at once."""
    payload: NotRequired[Literal["summary", "full"]]
    """How much of a message `email.received` and `email.sent` carry. `summary` is the addresses,
    subject and snippet; `full` adds `data.email`, the email as `GET
    /emails/{id}?include=attachment_content` returns it, so a handler has no second call to make.
    Every other event is the same either way, and an endpoint whose `format` is `v1` cannot be
    `full`.
    """


class RotateWebhookSecretRequest(TypedDict):
    grace_seconds: NotRequired[int]
    """Seconds the old secret keeps verifying: a day by default, a week at most, 0 after a leak."""


class RetryDeliveriesRequest(TypedDict):
    delivery_ids: list[str]
    """The deliveries to replay, at most 100."""


class WebhookTestRequest(TypedDict):
    event_type: WebhookEventType
    """The event type to deliver."""
    resource_id: NotRequired[str]
    """The id the test event is about."""
    payload: NotRequired[dict[str, Any]]
    """The event's `data`, sent verbatim."""


class SuppressionRequest(TypedDict):
    addresses: list[str]
    """The addresses to suppress, at most 1,000."""
    key: NotRequired[str]
    """The list: a `suppression_key` your sends name, or `*` for the workspace-wide one."""
    space_id: NotRequired[str]
    """Which space a created resource goes in. Omitted, the workspace itself."""
    scope: NotRequired[SuppressionScope]
    """`all` stops every send; `optional` only sends marked `unsubscribe`."""
    note: NotRequired[str]
    """Why the addresses are listed, for your records."""


class PacingRuleRequestHours(TypedDict):
    name: str
    """The rule's name."""
    space_id: NotRequired[str]
    """Which space a created resource goes in. Omitted, the workspace itself."""
    enabled: NotRequired[bool]
    """Whether the rule applies. A disabled one holds nothing and takes no plan allowance."""
    match: list[PacingMatch]
    """Which sends the rule reads, such as `[{"field":"to","pattern":"..."}]`. `[]` catches nothing;
    `[{"field":"from","pattern":"*"}]` catches every send.
    """
    kind: Literal["hours"]
    """`hours` holds mail outside weekly windows."""
    schedule: PacingSchedule
    """An `hours` rule's weekly windows, such as
    `{"timezone":"Europe/Berlin","windows":[{"days":[0,1,2,3,4],"start_minute":540,"end_minute":1020}]}`.
    """


class PacingRuleRequestLimit(TypedDict):
    name: str
    """The rule's name."""
    space_id: NotRequired[str]
    """Which space a created resource goes in. Omitted, the workspace itself."""
    enabled: NotRequired[bool]
    """Whether the rule applies. A disabled one holds nothing and takes no plan allowance."""
    match: list[PacingMatch]
    """Which sends the rule reads, such as `[{"field":"to","pattern":"..."}]`. `[]` catches nothing;
    `[{"field":"from","pattern":"*"}]` catches every send.
    """
    kind: Literal["limit"]
    """`limit` caps sends per rolling window."""
    limit: PacingLimit
    """A `limit` rule's cap, such as `{"scope":"to_domain","amount":100,"per_seconds":3600}`."""


PacingRuleRequest = PacingRuleRequestHours | PacingRuleRequestLimit


class UpdatePacingRuleRequest(TypedDict):
    name: NotRequired[str]
    """The rule's name."""
    enabled: NotRequired[bool]
    """Whether the rule applies. A disabled one holds nothing and takes no plan allowance."""
    match: NotRequired[list[PacingMatch]]
    """Which sends the rule reads, such as `[{"field":"to","pattern":"..."}]`. `[]` catches nothing;
    `[{"field":"from","pattern":"*"}]` catches every send.
    """
    kind: NotRequired[Literal["hours", "limit"]]
    """`hours` holds mail outside weekly windows; `limit` caps sends per rolling window."""
    schedule: NotRequired[PacingSchedule]
    """An `hours` rule's weekly windows, such as
    `{"timezone":"Europe/Berlin","windows":[{"days":[0,1,2,3,4],"start_minute":540,"end_minute":1020}]}`.
    """
    limit: NotRequired[PacingLimit]
    """A `limit` rule's cap, such as `{"scope":"to_domain","amount":100,"per_seconds":3600}`."""


class PacingSpreadRequest(TypedDict):
    spread: int
    """Randomness in send timing, 0 to 100: 0 is a metronome."""


class PacingReleaseRequest(TypedDict):
    email_ids: list[str]
    """The held emails to release, at most 500."""
    count_toward_limits: NotRequired[bool]
    """Whether released mail uses up the rules' budget."""


class UpdateWorkspaceRequestTracking(TypedDict):
    opens: NotRequired[bool]
    clicks: NotRequired[bool]


class UpdateWorkspaceRequest(TypedDict):
    name: NotRequired[str]
    """The workspace's name."""
    tracking: NotRequired[UpdateWorkspaceRequestTracking]
    """What a domain added from now on starts with. Only the fields given change; existing domains
    keep theirs.
    """


class UpdateMemberRequest(TypedDict):
    role: MemberRole


class CreateInvitationRequest(TypedDict):
    email: str
    """The address to invite."""
    role: NotRequired[MemberRole]


class ProblemIssuesItem(TypedDict):
    path: str
    message: str


class Problem(TypedDict):
    type: str
    title: str
    status: int
    detail: str
    code: str
    request_id: str
    issues: NotRequired[list[ProblemIssuesItem]]


class Space(TypedDict):
    """A group of domains, mailboxes and mail — one per customer, typically. Optional: a workspace
    that never creates one sees `space_id: null` everywhere.
    """

    id: str
    name: str
    external_id: str | None
    """Your own id for the customer, if you set one."""
    created_at: str


SpacePage = CursorPage[Space]


class ApiKey(TypedDict):
    id: str
    name: str
    scope: ApiKeyScope
    prefix: str
    last_used_at: str | None
    created_at: str


class ApiKeyCreated(TypedDict):
    """A newly issued key. The full `key` is returned only once."""

    id: str
    name: str
    scope: ApiKeyScope
    prefix: str
    last_used_at: str | None
    created_at: str
    key: str


ApiKeyPage = CursorPage[ApiKey]


Email = TypedDict(
    "Email",
    {
        "id": str,
        "thread_id": str,
        "space_id": str | None,
        "direction": EmailDirection,
        "status": EmailStatus,
        "from": EmailAddress,
        "to": list[str],
        "delivered_to": list[str],
        "cc": NotRequired[list[str]],
        "bcc": NotRequired[list[str]],
        "reply_to": NotRequired[list[str]],
        "subject": str,
        "snippet": str,
        "html": NotRequired[str | None],
        "text": NotRequired[str | None],
        "category": EmailCategory | None,
        "verdicts": EmailVerdicts | None,
        "verification": EmailVerification | None,
        "unavailable": EmailUnavailable | None,
        "suppression_key": str | None,
        "message_id": str,
        "in_reply_to": str | None,
        "idempotency_key": str | None,
        "created_at": str,
        "scheduled_at": str | None,
        "sent_at": str | None,
        "draft": EmailDraft | None,
        "attachments": NotRequired[list[Attachment]],
    },
)


SendEmailResponse = TypedDict(
    "SendEmailResponse",
    {
        "id": str,
        "thread_id": str,
        "space_id": str | None,
        "direction": EmailDirection,
        "status": EmailStatus,
        "from": EmailAddress,
        "to": list[str],
        "delivered_to": list[str],
        "cc": NotRequired[list[str]],
        "bcc": NotRequired[list[str]],
        "reply_to": NotRequired[list[str]],
        "subject": str,
        "snippet": str,
        "html": NotRequired[str | None],
        "text": NotRequired[str | None],
        "category": EmailCategory | None,
        "verdicts": EmailVerdicts | None,
        "verification": EmailVerification | None,
        "unavailable": EmailUnavailable | None,
        "suppression_key": str | None,
        "message_id": str,
        "in_reply_to": str | None,
        "idempotency_key": str | None,
        "created_at": str,
        "scheduled_at": str | None,
        "sent_at": str | None,
        "draft": EmailDraft | None,
        "attachments": NotRequired[list[Attachment]],
        "suppressed": list[str],
        "pacing": EmailPacing | None,
    },
)


EmailPage = CursorPage[Email]


class Thread(TypedDict):
    id: str
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    subject: str
    mailbox: str
    participants: list[str]
    message_count: int
    last_message_at: str
    forward_of: str | None
    """The thread this one was forwarded from, when a forward opened it."""
    messages: NotRequired[list[FullEmail]]
    messages_next_cursor: NotRequired[str | None]


class FullThread(TypedDict):
    id: str
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    subject: str
    mailbox: str
    participants: list[str]
    message_count: int
    last_message_at: str
    forward_of: str | None
    """The thread this one was forwarded from, when a forward opened it."""
    messages: list[FullEmail]
    messages_next_cursor: str | None


ThreadPage = CursorPage[Thread]


class Domain(TypedDict):
    id: str
    name: str
    region: MailRegion
    """Where the domain's mail is handled today. A domain carried over from the previous aiinbx
    reports `us-east-1` until its records verify here, then the region chosen for it.
    """
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    parent_id: str | None
    """The wildcard this subdomain is filed under, when it is one."""
    provided: bool
    """Whether this is the domain the workspace was given — `<slug>.aiinbx.app`. Verified through
    our own zone, so it has no records and cannot be deleted.
    """
    verified_at: str | None
    dkim_missing_since: str | None
    """When the DKIM record of this verified domain, or of its wildcard, was found missing from DNS.
    The domain keeps sending meanwhile. Null while the record resolves.
    """
    stops_sending_at: str | None
    """When the domain is lost if the DKIM record is not restored: 72 hours after
    `dkim_missing_since`. Then `verified_at` goes null and `domain.lost` is sent.
    """
    created_at: str
    tracking: DomainTracking
    records: NotRequired[list[DnsRecord]]


DomainPage = CursorPage[Domain]


class DnsDiagnosticsResponse(TypedDict):
    data: list[DnsFinding]


class MailboxAliasesItem(TypedDict):
    address: str
    name: str | None


class Mailbox(TypedDict):
    id: str
    provider: MailboxProvider
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    address: str
    name: str | None
    aliases: list[MailboxAliasesItem]
    state: MailboxState
    state_reason: str | None
    region: MailRegion
    app_id: str | None
    ref: str | None
    metadata: dict[str, str]
    """Your own key-value pairs, stored and given back as they are. Up to 50 keys; a key is 1–40
    characters, a value up to 500. Written whole: what you send replaces what was there.
    """
    connected_at: str
    last_sync_at: str | None


MailboxPage = CursorPage[Mailbox]


class MailboxSyncResponse(TypedDict):
    status: Literal["queued"]


class ConnectMailboxResponse(TypedDict):
    url: str


class OAuthApp(TypedDict):
    id: str
    provider: MailboxProvider
    name: str
    slug: str
    client_id: str
    tenant: str | None
    pubsub_topic: str | None
    accent: str | None
    tagline: str | None
    support_email: str | None
    logo_url: str | None
    """A logo linked from the customer's own server. An uploaded one is served from us and is not
    linkable through the API.
    """
    connect_url: str
    return_urls: list[str]
    """The pages a connect link — `connect_url` + `/start?return_to=…` — may return to. Matched on
    origin and path.
    """
    redirect_uri: str
    push_endpoint: str | None
    created_at: str


OAuthAppPage = CursorPage[OAuthApp]


class WebhookEndpoint(TypedDict):
    id: str
    url: str
    enabled: bool
    format: Literal["v2", "v1"]
    """Read-only. `v1` marks an endpoint carried over from the previous aiinbx.com: it receives that
    system's bodies and can subscribe only to the events it had — `email.received`,
    `email.delivered`, `email.bounced`, `email.complained`, `email.failed`, `email.opened`,
    `email.clicked`. Endpoints created here are `v2`.
    """
    subscriptions: list[WebhookEventType]
    routing: list[WebhookRoutingRule]
    max_concurrency: int
    payload: Literal["summary", "full"]
    """How much of a message `email.received` and `email.sent` carry. `summary` is the addresses,
    subject and snippet; `full` adds `data.email`, the email as `GET
    /emails/{id}?include=attachment_content` returns it, so a handler has no second call to make.
    Every other event is the same either way, and an endpoint whose `format` is `v1` cannot be
    `full`.
    """
    previous_secret_expires_at: str | None
    created_at: str
    updated_at: str
    secret: NotRequired[str]


class WebhookEndpointCreated(TypedDict):
    """A newly created endpoint. Its signing `secret` is returned only once."""

    id: str
    url: str
    enabled: bool
    format: Literal["v2", "v1"]
    """Read-only. `v1` marks an endpoint carried over from the previous aiinbx.com: it receives that
    system's bodies and can subscribe only to the events it had — `email.received`,
    `email.delivered`, `email.bounced`, `email.complained`, `email.failed`, `email.opened`,
    `email.clicked`. Endpoints created here are `v2`.
    """
    subscriptions: list[WebhookEventType]
    routing: list[WebhookRoutingRule]
    max_concurrency: int
    payload: Literal["summary", "full"]
    """How much of a message `email.received` and `email.sent` carry. `summary` is the addresses,
    subject and snippet; `full` adds `data.email`, the email as `GET
    /emails/{id}?include=attachment_content` returns it, so a handler has no second call to make.
    Every other event is the same either way, and an endpoint whose `format` is `v1` cannot be
    `full`.
    """
    previous_secret_expires_at: str | None
    created_at: str
    updated_at: str
    secret: str


WebhookEndpointPage = CursorPage[WebhookEndpoint]


class WebhookEventEmailReceived(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.received"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailReceivedEventData


class WebhookEventEmailSent(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.sent"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailSentEventData


class WebhookEventEmailDelivered(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.delivered"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailDeliveredEventData


class WebhookEventEmailBounced(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.bounced"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailBouncedEventData


class WebhookEventEmailComplained(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.complained"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailComplainedEventData


class WebhookEventEmailFailed(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.failed"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailFailedEventData


class WebhookEventEmailUnsubscribed(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.unsubscribed"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailUnsubscribedEventData


class WebhookEventEmailOpened(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.opened"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailOpenedEventData


class WebhookEventEmailClicked(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["email.clicked"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: EmailClickedEventData


class WebhookEventThreadCreated(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["thread.created"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: ThreadCreatedEventData


class WebhookEventDomainVerified(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["domain.verified"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: DomainEventData


class WebhookEventDomainAtRisk(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["domain.at_risk"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: DomainAtRiskEventData


class WebhookEventDomainRestored(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["domain.restored"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: DomainEventData


class WebhookEventDomainLost(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["domain.lost"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: DomainEventData


class WebhookEventMailboxConnected(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["mailbox.connected"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: MailboxConnectedEventData


class WebhookEventMailboxNeedsReauth(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["mailbox.needs_reauth"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: MailboxStateEventData


class WebhookEventMailboxDisconnected(TypedDict):
    id: str
    """The event, `evt_…`. Stable across retries and replays: deduplicate on it."""
    type: Literal["mailbox.disconnected"]
    created_at: str
    """When the event happened."""
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    data: MailboxStateEventData


WebhookEvent = WebhookEventEmailReceived | WebhookEventEmailSent | WebhookEventEmailDelivered | WebhookEventEmailBounced | WebhookEventEmailComplained | WebhookEventEmailFailed | WebhookEventEmailUnsubscribed | WebhookEventEmailOpened | WebhookEventEmailClicked | WebhookEventThreadCreated | WebhookEventDomainVerified | WebhookEventDomainAtRisk | WebhookEventDomainRestored | WebhookEventDomainLost | WebhookEventMailboxConnected | WebhookEventMailboxNeedsReauth | WebhookEventMailboxDisconnected


class WebhookDelivery(TypedDict):
    id: str
    event_id: str
    event_type: WebhookEventType
    resource_id: str
    """What the event is about: the email, thread, domain or mailbox, or for `email.unsubscribed`
    the suppression. A test event's is the `resource_id` it was sent with.
    """
    state: DeliveryState
    next_attempt_at: str | None
    created_at: str
    body: WebhookEvent | dict[str, Any] | None
    """The event envelope the endpoint receives, as stored: a `full` endpoint's is shown without
    `data.email`, which is read from the message when a delivery is sent and not kept. Null for a
    `v1` endpoint in a listing — its legacy body is built from the message when it is sent and is
    not stored — and for a delivery nothing was sent for: a `v1` endpoint's event whose subject
    no longer exists is settled as failed with no attempts.
    """
    attempts: list[WebhookAttempt]


WebhookDeliveryPage = CursorPage[WebhookDelivery]


class WebhookSecretResponse(TypedDict):
    secret: str
    previous_secret_expires_at: str | None


class WebhookTestResponse(TypedDict):
    delivery_id: str
    state: DeliveryState
    status_code: int | None
    duration_ms: int | None
    error: str | None
    response: str | None


EventPage = CursorPage[WebhookEvent]


class Suppression(TypedDict):
    id: str
    address: str
    key: str
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    reason: SuppressionReason
    scope: SuppressionScope
    note: str | None
    blocks: int
    last_blocked_at: str | None
    source_email_id: str | None
    created_at: str


SuppressionPage = CursorPage[Suppression]


class SuppressionBatch(TypedDict):
    data: list[Suppression]


class SuppressionDeleted(TypedDict):
    id: str
    provider_suppressed: bool | None
    """True when SES still refuses the address off its own suppression list, which keeps addresses
    that hard-bounced as dead: sends to it keep failing as `bad_address` bounces whatever your
    lists say. Null when that could not be checked just now.
    """


class PacingRuleHours(TypedDict):
    id: str
    name: str
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    enabled: bool
    builtin: bool
    match: list[PacingMatch]
    created_at: str
    kind: Literal["hours"]
    schedule: PacingScheduleState


class PacingRuleLimit(TypedDict):
    id: str
    name: str
    space_id: str | None
    """Which space a resource is in. Null is the workspace itself — what every resource of a
    workspace that has no spaces says.
    """
    enabled: bool
    builtin: bool
    match: list[PacingMatch]
    created_at: str
    kind: Literal["limit"]
    """`limit` caps sends per rolling window."""
    limit: PacingLimit
    """A `limit` rule's cap, such as `{"scope":"to_domain","amount":100,"per_seconds":3600}`."""


PacingRule = PacingRuleHours | PacingRuleLimit


PacingRulePage = CursorPage[PacingRule]


class PacingSpread(TypedDict):
    spread: int


class PacingQueue(TypedDict):
    data: list[PacingQueueItem]
    total: int
    sampled: int
    as_of: str
    spread: int
    rules: list[PacingRule]
    rule_counts: list[PacingRuleCount]


class IdListResponse(TypedDict):
    data: list[str]


class Workspace(TypedDict):
    """A workspace: the account that owns everything else."""

    id: str
    name: str
    slug: str
    """The handle in console URLs. It follows the name; the provided domain keeps the slug the
    workspace was created with.
    """
    role: WorkspaceRole | None
    """What the caller may do here: the role of the person a token acts for. Null for an API key,
    which acts with its creator's current rights: admin-only operations answer 403 once the
    creator is no longer an admin or has left.
    """
    tracking: DomainTracking
    """What a domain added from now on starts with."""
    inboxes: list[Inbox] | None
    """The inboxes the caller is held to here, when it was connected as an inbox: it reads their
    mail and sends as them, and nothing else. Null for a connection to the whole workspace, and
    for an API key.
    """
    created_at: str


class WorkspaceList(TypedDict):
    data: list[Workspace]
    mode: ConnectionMode


class Member(TypedDict):
    id: str
    name: str
    email: str
    role: WorkspaceRole
    joined_at: str
    last_active_at: str | None
    """When they last used the console. Null if they never have."""


class MemberList(TypedDict):
    data: list[Member]


class Invitation(TypedDict):
    id: str
    email: str
    role: MemberRole
    invited_by: str
    """Who sent it, by name — or email when they gave none."""
    created_at: str
    expires_at: str


class InvitationList(TypedDict):
    data: list[Invitation]
