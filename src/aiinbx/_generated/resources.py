# Generated from @workspace/api-contract by `bun run sdk:generate`. Do not edit.
# mypy: warn_return_any=False
from __future__ import annotations

from collections.abc import AsyncIterator, Iterator, Sequence
from typing import Literal

from .._base import (
    AsyncRawResource,
    AsyncResource,
    RawResponse,
    SyncRawResource,
    SyncResource,
    Timeout,
    idempotency_headers,
    iterate_pages,
    iterate_pages_async,
    path_segment,
    wire,
)
from ..models import (
    ApiKey,
    ApiKeyCreated,
    ApiKeyPage,
    ConnectMailboxRequest,
    ConnectMailboxResponse,
    CreateApiKeyRequest,
    CreateDomainRequest,
    CreateInvitationRequest,
    CreateOAuthAppRequest,
    CreateSpaceRequest,
    DnsDiagnosticsResponse,
    Domain,
    DomainPage,
    Email,
    EmailPage,
    EventPage,
    ForwardThreadRequest,
    FullEmail,
    FullThread,
    IdListResponse,
    Invitation,
    InvitationList,
    Mailbox,
    MailboxPage,
    MailboxSyncResponse,
    Member,
    MemberList,
    OAuthApp,
    OAuthAppPage,
    PacingQueue,
    PacingReleaseRequest,
    PacingRule,
    PacingRulePage,
    PacingRuleRequest,
    PacingSpread,
    PacingSpreadRequest,
    ReplyThreadRequest,
    RetryDeliveriesRequest,
    RotateWebhookSecretRequest,
    SendDraftRequest,
    SendEmailRequest,
    SendEmailResponse,
    Space,
    SpacePage,
    Suppression,
    SuppressionBatch,
    SuppressionDeleted,
    SuppressionPage,
    SuppressionRequest,
    Thread,
    ThreadPage,
    UpdateDomainRequest,
    UpdateEmailRequest,
    UpdateMemberRequest,
    UpdateOAuthAppRequest,
    UpdatePacingRuleRequest,
    UpdateSpaceRequest,
    UpdateWebhookEndpointRequest,
    UpdateWorkspaceRequest,
    WebhookDelivery,
    WebhookDeliveryPage,
    WebhookEndpoint,
    WebhookEndpointCreated,
    WebhookEndpointPage,
    WebhookEndpointRequest,
    WebhookEvent,
    WebhookSecretResponse,
    WebhookTestRequest,
    WebhookTestResponse,
    Workspace,
    WorkspaceList,
)

__all__ = [
    "ApiKeys",
    "AsyncApiKeys",
    "AsyncAttachments",
    "AsyncDomains",
    "AsyncEmails",
    "AsyncEvents",
    "AsyncInvitations",
    "AsyncMailboxes",
    "AsyncMembers",
    "AsyncOauthApps",
    "AsyncPacing",
    "AsyncPacingRules",
    "AsyncRawApiKeys",
    "AsyncRawAttachments",
    "AsyncRawDomains",
    "AsyncRawEmails",
    "AsyncRawEvents",
    "AsyncRawInvitations",
    "AsyncRawMailboxes",
    "AsyncRawMembers",
    "AsyncRawOauthApps",
    "AsyncRawPacing",
    "AsyncRawPacingRules",
    "AsyncRawSpaces",
    "AsyncRawSuppressions",
    "AsyncRawThreads",
    "AsyncRawWebhookEndpoints",
    "AsyncRawWorkspaces",
    "AsyncSpaces",
    "AsyncSuppressions",
    "AsyncWebhookEndpoints",
    "AsyncWorkspaces",
    "Attachments",
    "Domains",
    "Emails",
    "Events",
    "GeneratedAsyncThreads",
    "GeneratedThreads",
    "Invitations",
    "Mailboxes",
    "Members",
    "OauthApps",
    "Pacing",
    "PacingRules",
    "RawApiKeys",
    "RawAttachments",
    "RawDomains",
    "RawEmails",
    "RawEvents",
    "RawInvitations",
    "RawMailboxes",
    "RawMembers",
    "RawOauthApps",
    "RawPacing",
    "RawPacingRules",
    "RawSpaces",
    "RawSuppressions",
    "RawThreads",
    "RawWebhookEndpoints",
    "RawWorkspaces",
    "Spaces",
    "Suppressions",
    "WebhookEndpoints",
    "Workspaces",
]


class Spaces(SyncResource):
    """Group a workspace's domains, mailboxes and mail by customer. Optional: a workspace that is
    not a platform never needs one.
    """

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        external_id: str | None = None,
        timeout: Timeout = None,
    ) -> SpacePage:
        """List spaces.

        Lists the workspace's spaces, oldest first. Filter by `external_id` to find the one that
        stands for a customer of yours.
        """
        return self._request(
            "GET",
            "/spaces",
            params={
                "limit": limit,
                "cursor": cursor,
                "external_id": external_id,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        external_id: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[Space]:
        """List spaces, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                external_id=external_id,
                timeout=timeout,
            )
        )

    def create(
        self,
        params: CreateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> Space:
        """Create a space.

        Creates a space — one per customer, typically. Domains, mailboxes, rules and suppressions
        are put in a space with `space_id` when they are created, and every email and thread
        inherits the space of the domain or mailbox it went through. Anything created without a
        `space_id` belongs to the workspace itself and `space_id` reads as null. API keys and
        webhook endpoints belong to the workspace. `external_id` is your own id for the customer:
        unique per workspace, so a second space for the same customer is `409 external_id_taken`,
        and the space can be found by it with `GET /spaces?external_id=`.
        """
        return self._request(
            "POST",
            "/spaces",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> Space:
        """Retrieve a space.

        Returns one space by id, with its name and the `external_id` you gave it.
        """
        return self._request(
            "GET",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )

    def update(
        self,
        space_id: str,
        params: UpdateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> Space:
        """Update a space.

        Changes the space's name or `external_id`; only the fields given change, and
        `external_id: null` clears it. Nothing in the space moves.
        """
        return self._request(
            "PATCH",
            f"/spaces/{path_segment(space_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a space.

        Marks the space for deletion and starts its teardown in the background. The space
        immediately stops accepting work and no longer appears in the API; its domains then come
        off DNS verification and sending, its mailboxes are disconnected, and its emails,
        threads, rules and suppressions are removed. A wildcard domain in the space is deleted
        with its subdomains, including any filed in other spaces. Admin only.
        """
        return self._request(
            "DELETE",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )


class ApiKeys(SyncResource):
    """Create and delete credentials for API access."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> ApiKeyPage:
        """List API keys.

        Lists the workspace's API keys, newest first. Keys are returned as metadata only — the
        prefix, scope, creation time, and `last_used_at`; the secret itself is never readable
        after creation. Admin only.
        """
        return self._request(
            "GET",
            "/api-keys",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        timeout: Timeout = None,
    ) -> Iterator[ApiKey]:
        """List API keys, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                timeout=timeout,
            )
        )

    def create(
        self,
        params: CreateApiKeyRequest,
        *,
        timeout: Timeout = None,
    ) -> ApiKeyCreated:
        """Create an API key.

        Creates an organization-wide API key and returns its secret exactly once, in the `key`
        field. Store it before the response is discarded — it cannot be recovered. Choose the
        narrowest scope the caller needs: `read`, `sending`, or `full`. The key reaches the whole
        workspace, spaces included. Admin only.
        """
        return self._request(
            "POST",
            "/api-keys",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        key_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete an API key.

        Deletes a key immediately. It authenticates nothing afterwards and cannot be recovered;
        issue a new key instead. Admin only.
        """
        return self._request(
            "DELETE",
            f"/api-keys/{path_segment(key_id)}",
            timeout=timeout,
        )


class Emails(SyncResource):
    """Send, inspect, and schedule email."""

    def send(
        self,
        params: SendEmailRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> SendEmailResponse:
        """Send an email.

        Sends an email — or, with `draft: true`, writes it for a person to review and send.
        Requires a `from` address on a verified domain or a connected mailbox, and at least one
        of `html` or `text`. `thread_id` continues a conversation; to answer a message AI Inbx
        has not seen — mail from before a migration, or from another provider — name it in
        `in_reply_to` and `references` instead. Recipients on a matching suppression list are
        dropped and reported in `suppressed`; a pacing rule that holds the message is reported in
        `pacing`. Pass `Idempotency-Key` so a retry after a timeout replays the original send
        instead of sending twice. A workspace with no plan fails with 402 `plan_required`, and
        one that has used its plan's emails for the month with 402 `allowance_reached`.
        """
        return self._request(
            "POST",
            "/emails",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        direction: Literal["inbound", "outbound"] | None = None,
        status: Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"] | None = None,
        thread_id: str | None = None,
        query: str | None = None,
        timeout: Timeout = None,
    ) -> EmailPage:
        """List emails.

        Lists emails in the workspace, newest first. Filter by `direction`, delivery `status`, a
        single `thread_id`, or a literal `query`: every word in it must appear in the subject,
        the sender, a recipient or the Message-ID, in any order and case. The query is a literal
        filter; the API does not provide semantic email search. To sync, walk forward instead:
        `order=asc` with `after` set to the `created_at` of the last email you have lists only
        what is new, oldest first.
        """
        return self._request(
            "GET",
            "/emails",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "direction": direction,
                "status": status,
                "thread_id": thread_id,
                "query": query,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        direction: Literal["inbound", "outbound"] | None = None,
        status: Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"] | None = None,
        thread_id: str | None = None,
        query: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[Email]:
        """List emails, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                after=after,
                before=before,
                order=order,
                direction=direction,
                status=status,
                thread_id=thread_id,
                query=query,
                timeout=timeout,
            )
        )

    def retrieve(
        self,
        email_id: str,
        *,
        include: Sequence[Literal["attachment_content"]] | None = None,
        timeout: Timeout = None,
    ) -> FullEmail:
        """Retrieve an email.

        Returns one email in full: both bodies, every header, attachments, the delivery event
        history, and tracked engagements. Pass `include=attachment_content` to inline each
        attachment's prepared text, which saves a request per attachment before handing a message
        to a model.
        """
        return self._request(
            "GET",
            f"/emails/{path_segment(email_id)}",
            params={
                "include": include,
            },
            timeout=timeout,
        )

    def update(
        self,
        email_id: str,
        params: UpdateEmailRequest,
        *,
        timeout: Timeout = None,
    ) -> Email:
        """Update an email.

        Changes an email that has not gone out — a `draft` or a `scheduled` one: its recipients,
        subject, bodies, attachments or send time. Fields left out stay as they are. The email is
        composed again when it goes, so what is sent is what it says by then. One that has begun
        sending, or was canceled or discarded, returns 409 `not_scheduled`.
        """
        return self._request(
            "PATCH",
            f"/emails/{path_segment(email_id)}",
            json=params,
            timeout=timeout,
        )

    def send_draft(
        self,
        email_id: str,
        params: SendDraftRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> Email:
        """Send a draft.

        Sends a draft: at the `scheduled_at` given, else at the draft's own while it is still
        ahead, else now. From here it is a `scheduled` email — counted against the plan, and
        composed again when it goes. Anything but a draft returns 409 `not_draft`; a workspace
        out of emails returns 402.
        """
        return self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/send",
            json=params or {},
            timeout=timeout,
        )

    def cancel(
        self,
        email_id: str,
        *,
        timeout: Timeout = None,
    ) -> Email:
        """Cancel an email.

        Cancels a scheduled email before it is composed and sent — its status becomes `canceled`
        — or discards a draft, which becomes `discarded`. Either is terminal: the email cannot be
        put back into flight.
        """
        return self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/cancel",
            timeout=timeout,
        )


class GeneratedThreads(SyncResource):
    """Read email conversations."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        query: str | None = None,
        mailbox: str | None = None,
        timeout: Timeout = None,
    ) -> ThreadPage:
        """List threads.

        Lists conversations, most recently active first. Every word of `query` must appear in the
        subject, the mailbox or a participant's address, literally and in any order; `mailbox`
        narrows to one address.
        """
        return self._request(
            "GET",
            "/threads",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "query": query,
                "mailbox": mailbox,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        query: str | None = None,
        mailbox: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[Thread]:
        """List threads, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                query=query,
                mailbox=mailbox,
                timeout=timeout,
            )
        )

    def retrieve(
        self,
        thread_id: str,
        *,
        message_limit: int | None = None,
        message_cursor: str | None = None,
        timeout: Timeout = None,
    ) -> FullThread:
        """Retrieve a thread.

        Returns a thread with its messages inline, oldest first. Messages paginate independently
        of the thread list via `message_limit` and `message_cursor`, so a long conversation can
        be walked without loading it whole.
        """
        return self._request(
            "GET",
            f"/threads/{path_segment(thread_id)}",
            params={
                "message_limit": message_limit,
                "message_cursor": message_cursor,
            },
            timeout=timeout,
        )

    def reply(
        self,
        thread_id: str,
        params: ReplyThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> SendEmailResponse:
        """Reply in a thread.

        Replies within a thread. The sender, recipients, subject, and the `In-Reply-To` and
        `References` headers are inferred from the conversation, as a mail client infers them
        from the email answered: `email_id`, or the thread's latest. The reply follows that
        email's Reply-To; one that names only your own addresses is refused with 400
        `no_recipients` rather than guessed around. Only the content is required — set
        `reply_all` or the individual fields to override what is inferred. Suppression and pacing
        behave exactly as on a send; an `Idempotency-Key` is bound to the request, so a retry
        replays the reply even after the thread has moved on. So does the plan: 402
        `plan_required` without one, 402 `allowance_reached` once its emails are used up.
        """
        return self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/reply",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    def forward(
        self,
        thread_id: str,
        params: ForwardThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> SendEmailResponse:
        """Forward a thread.

        Sends the whole thread as one email to recipients who were not on it. Every message is
        rendered into one transcript, oldest first, each turn as what its author wrote with
        quoted tails and repeated signatures removed; the thread's attachments ride along unless
        `include_attachments` is false, and `note` is placed above the transcript. Only `to` is
        required: the sender defaults to the thread's mailbox and the subject to `Fwd:` and the
        thread's. The forward opens a thread of its own, linked back through `forward_of`, so a
        later reply on the original still goes to its participants and replies to the forward
        land on the forward. Suppression, pacing, scheduling, and idempotency behave exactly as
        on a send. So does the plan: 402 `plan_required` without one, 402 `allowance_reached`
        once its emails are used up.
        """
        return self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/forward",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )


class Domains(SyncResource):
    """Manage sending domains and DNS checks."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> DomainPage:
        """List domains.

        Lists the workspace's sending domains with their verification state and tracking
        settings.
        """
        return self._request(
            "GET",
            "/domains",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[Domain]:
        """List domains, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                timeout=timeout,
            )
        )

    def create(
        self,
        params: CreateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Create a domain.

        Registers a sending domain and returns the DNS records to publish: SPF, DKIM, DMARC, a
        return path, and an MX record for receiving. `region` selects the regional mail
        infrastructure for this domain; it can be changed with `PATCH /domains/{domain_id}` until
        the domain is verified.

        A wildcard — `*.acme.dev` — is verified once and covers every subdomain: the MX record
        goes at `*.acme.dev`, the rest at `acme.dev`, and the apex keeps whatever mail setup it
        has. A name one label under a wildcard of yours — `hi.acme.dev` under `*.acme.dev` — is
        created as a subdomain of it: no records, verified as soon as the wildcard is, in
        whatever `space_id` you give it. That is how a platform hands each customer an address of
        their own without touching DNS again.

        A domain name can be connected in several spaces and workspaces, but sending and
        receiving are enabled for the one whose DKIM key is published. To move them, add the
        domain where it should go and publish its DNS records. The next verification check moves
        them; existing mail stays where it was. Duplicate apex or wildcard identities within one
        space fail with `domain_taken`.

        Every workspace already has one domain it did not add: `<slug>.aiinbx.app`, listed with
        `provided: true`. It is verified through our zone, has no records and cannot be deleted;
        a name under `aiinbx.app` cannot be added by hand and fails with `reserved_domain`.

        A domain of its own counts against the plan's custom domains — a subdomain under a
        wildcard and the provided domain do not. With none left the request fails with 402
        `allowance_reached`, and a workspace with no plan with 402 `plan_required`.

        `track_opens` and `track_clicks` set the domain's `tracking`; what they leave out starts
        as the workspace's tracking defaults in the console say — off unless they are set there —
        or, on a subdomain, as its wildcard's. Change either afterwards with `PATCH
        /domains/{domain_id}`.
        """
        return self._request(
            "POST",
            "/domains",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Retrieve a domain.

        Returns one domain with its DNS records and the state of each — `pending`, `verified`, or
        `missing` — along with when each was last checked.
        """
        return self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    def update(
        self,
        domain_id: str,
        params: UpdateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Update domain tracking settings.

        Updates whether opens and clicks are tracked on mail sent from the domain. Applies to
        every send from it that does not say otherwise in `tracking`, from the next one to leave.
        At least one field is required.
        """
        return self._request(
            "PATCH",
            f"/domains/{path_segment(domain_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a domain.

        Deletes a domain and stops future sends from it. Remove the published DNS records
        afterwards. A wildcard's subdomains are deleted with it, in whatever space they sit; a
        subdomain is removed on its own, with nothing to unpublish. The provided domain cannot be
        deleted and fails with `domain_provided`.
        """
        return self._request(
            "DELETE",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    def verify(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Verify domain DNS records now.

        Checks the domain's DNS records against live DNS now. `verified_at` stays null until the
        sending identity’s DKIM verification succeeds; inbound MX, SPF, and DMARC readiness are
        separate. DNS propagation usually takes minutes and occasionally hours, so poll at a sane
        interval or subscribe to the `domain.verified` webhook instead. Domains are also
        rechecked in the background: a verified domain whose DKIM record stops resolving gets
        `dkim_missing_since`, keeps sending, and `domain.at_risk` is sent; `domain.restored`
        follows if the record is back, and has held for an hour, by `stops_sending_at`, otherwise
        it loses `verified_at` and `domain.lost` is sent.
        """
        return self._request(
            "POST",
            f"/domains/{path_segment(domain_id)}/verify",
            timeout=timeout,
        )

    def diagnostics(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> DnsDiagnosticsResponse:
        """Diagnose domain DNS configuration.

        Reads the domain's live DNS zone and reports what is wrong with it — a duplicate SPF
        record, a permissive policy, a missing return path. Each finding carries a severity, an
        explanation, the fix, and the records it was drawn from. Nothing is stored; the result
        always reflects DNS as it is right now.
        """
        return self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}/diagnostics",
            timeout=timeout,
        )


class Mailboxes(SyncResource):
    """Connect and manage provider mailboxes."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> MailboxPage:
        """List mailboxes.

        Lists connected Gmail and Outlook mailboxes with their sync state.
        """
        return self._request(
            "GET",
            "/mailboxes",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[Mailbox]:
        """List mailboxes, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                timeout=timeout,
            )
        )

    def connect(
        self,
        params: ConnectMailboxRequest,
        *,
        timeout: Timeout = None,
    ) -> ConnectMailboxResponse:
        """Create a mailbox connection URL.

        Creates a single-use, short-lived URL that walks a customer through authorizing their
        Gmail or Outlook mailbox. Redirect them to it rather than emailing it. Pass `ref` — your
        own identifier — and `metadata` for anything else you want kept with the mailbox; both
        are stored on it and carried on every `mailbox.*` webhook. On a reconnect each replaces
        what the mailbox had, and one left out leaves it alone. The `mailbox.connected` webhook —
        not the browser returning to `return_to` — is the authoritative signal that the mailbox
        is live. `return_to` may be any URL here, since the request is authenticated; a connect
        link opened from a browser is held to the app's `return_urls` instead. `space_id` files
        the mailbox in a space; the returned URL carries it, so a platform mints one link per
        customer server-side rather than handing out the bare hosted link. A workspace with no
        plan fails with 402 `plan_required`. A mailbox counts against the plan's mailboxes, but
        which one it will be is only known once the person has authorized: with none left, a
        mailbox the workspace does not already hold is refused then, and the refusal is reported
        in `error` on `return_to`. Reconnecting one that is `active` or `needs_reauth` takes
        nothing new.
        """
        return self._request(
            "POST",
            "/mailboxes/connect",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> Mailbox:
        """Retrieve a mailbox.

        Returns one mailbox, including its `state` and the provider's `state_reason` when there
        is one. A mailbox that is not `active` cannot send.
        """
        return self._request(
            "GET",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    def disconnect(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> Mailbox:
        """Disconnect a mailbox.

        Disconnects a mailbox, stopping sync and dropping its stored credentials. Messages
        already received stay on their threads.
        """
        return self._request(
            "DELETE",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    def sync(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> MailboxSyncResponse:
        """Queue a mailbox sync.

        Queues a catch-up sync for a mailbox. Mail normally arrives on its own through provider
        push notifications, so this is a repair tool rather than a way to poll. Messages found
        surface as ordinary `email.received` events.
        """
        return self._request(
            "POST",
            f"/mailboxes/{path_segment(mailbox_id)}/sync",
            timeout=timeout,
        )


class OauthApps(SyncResource):
    """Manage customer-owned Google and Microsoft OAuth apps."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> OAuthAppPage:
        """List OAuth apps.

        Lists the workspace's own Google and Microsoft OAuth apps.
        """
        return self._request(
            "GET",
            "/oauth-apps",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        timeout: Timeout = None,
    ) -> Iterator[OAuthApp]:
        """List OAuth apps, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                timeout=timeout,
            )
        )

    def create(
        self,
        params: CreateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> OAuthApp:
        """Create an OAuth app.

        Registers your own OAuth app so the mailbox consent screen carries your product's name
        rather than AI Inbx. The response returns the `redirect_uri` to register with the
        provider, a hosted `connect_url`, and — for Google — the `push_endpoint` your own Pub/Sub
        topic should publish to. The `slug` is claimed globally because it forms the connect URL.
        `return_urls` lists the pages of yours a connect link (`connect_url` +
        `/start?return_to=…`) may send a person back to; without one, only the hosted page works.
        """
        return self._request(
            "POST",
            "/oauth-apps",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> OAuthApp:
        """Retrieve an OAuth app.

        Returns one OAuth app. The client secret is never returned.
        """
        return self._request(
            "GET",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )

    def update(
        self,
        app_id: str,
        params: UpdateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> OAuthApp:
        """Update an OAuth app.

        Updates an OAuth app's credentials, branding or return URLs. At least one field is
        required. A rotated secret replaces the old one immediately, so update the provider
        first. `return_urls` replaces the whole list.
        """
        return self._request(
            "PATCH",
            f"/oauth-apps/{path_segment(app_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete an OAuth app.

        Deletes an OAuth app. Mailboxes already connected through it keep working until their
        authorization lapses.
        """
        return self._request(
            "DELETE",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )


class WebhookEndpoints(SyncResource):
    """Configure event delivery and inspect delivery attempts."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> WebhookEndpointPage:
        """List webhook endpoints.

        Lists the workspace's webhook endpoints with their subscriptions and routing rules.
        """
        return self._request(
            "GET",
            "/webhook-endpoints",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        timeout: Timeout = None,
    ) -> Iterator[WebhookEndpoint]:
        """List webhook endpoints, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                timeout=timeout,
            )
        )

    def create(
        self,
        params: WebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> WebhookEndpointCreated:
        """Create a webhook endpoint.

        Registers an organization-wide endpoint and returns its signing secret exactly once, in
        the `secret` field: no later read shows it again. A secret that was lost, or has leaked,
        is replaced with `POST /webhook-endpoints/{endpoint_id}/rotate-secret`, which keeps the
        old one verifying for a grace period while you deploy the new one. `subscriptions` must
        name at least one event type. Setting `payload` to `full` puts the whole email on
        `email.received` and `email.sent`, as `data.email`, so a handler does not have to fetch
        it. Optional routing rules narrow delivery by sender or recipient: a matching `block`
        rule always wins, and an empty allow list means no opinion. The endpoint receives every
        space's events, each stamped with its `space_id`.
        """
        return self._request(
            "POST",
            "/webhook-endpoints",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> WebhookEndpoint:
        """Retrieve a webhook endpoint.

        Returns one endpoint, including when a rotated previous secret stops being accepted.
        """
        return self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    def update(
        self,
        endpoint_id: str,
        params: UpdateWebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> WebhookEndpoint:
        """Update a webhook endpoint.

        Updates an endpoint's URL, subscriptions, routing rules, payload, or enabled state. At
        least one field is required. A change of `payload` applies from the next delivery
        attempt, retries of earlier events included; a `v1` endpoint cannot be `full`. A disabled
        endpoint receives nothing, and events that occur while it is off are not queued for
        later.
        """
        return self._request(
            "PATCH",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a webhook endpoint.

        Deletes an endpoint. Pending deliveries to it stop.
        """
        return self._request(
            "DELETE",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    def rotate_secret(
        self,
        endpoint_id: str,
        params: RotateWebhookSecretRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> WebhookSecretResponse:
        """Rotate a webhook signing secret.

        Issues a new signing secret and returns it, once — the only way to get a secret after the
        endpoint was created. The previous one keeps verifying for `grace_seconds` (a day by
        default, a week at most): every delivery in that window is signed with both, so a
        deployment can roll over without dropping events, and `previous_secret_expires_at` says
        when the overlap ends. Set the grace period to 0 only when a secret has leaked and the
        exposure matters more than the gap.
        """
        return self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/rotate-secret",
            json=params or {},
            timeout=timeout,
        )

    def test(
        self,
        endpoint_id: str,
        params: WebhookTestRequest,
        *,
        timeout: Timeout = None,
    ) -> WebhookTestResponse:
        """Send a test webhook.

        Delivers a synthetic event to the endpoint and reports what it actually did — status
        code, duration, error, and the first 2 KB of its response. The test event is signed like
        a real one, so it exercises signature verification too. `payload` is sent verbatim and
        does not have to match the real shape for that event type. A test event is about no
        message, so on a `full` endpoint the `data.email` of an `email.received` or `email.sent`
        test is the `email` you put in `payload`, or null.
        """
        return self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/test",
            json=params,
            timeout=timeout,
        )

    def list_deliveries(
        self,
        endpoint_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        state: Literal["pending", "delivered", "failed"] | None = None,
        timeout: Timeout = None,
    ) -> WebhookDeliveryPage:
        """List webhook deliveries.

        Lists deliveries to an endpoint, filterable by state. Each carries the event envelope it
        sends and every attempt made: timestamp, status code, duration, error, and the beginning
        of your response, which is usually what explains a rejection. `body` is what is stored.
        For a `full` endpoint that is the envelope without `data.email`: the email is read from
        the message each time a delivery is sent and is not kept with it. It is null for a `v1`
        endpoint — its legacy body is built from the message at send time, not stored — and for a
        delivery nothing was sent for.
        """
        return self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries",
            params={
                "limit": limit,
                "cursor": cursor,
                "state": state,
            },
            timeout=timeout,
        )

    def iter_deliveries(
        self,
        endpoint_id: str,
        *,
        limit: int | None = None,
        state: Literal["pending", "delivered", "failed"] | None = None,
        timeout: Timeout = None,
    ) -> Iterator[WebhookDelivery]:
        """List webhook deliveries, every page."""
        yield from iterate_pages(
            lambda cursor: self.list_deliveries(
                endpoint_id,
                cursor=cursor,
                limit=limit,
                state=state,
                timeout=timeout,
            )
        )

    def retry_deliveries(
        self,
        endpoint_id: str,
        params: RetryDeliveriesRequest,
        *,
        timeout: Timeout = None,
    ) -> IdListResponse:
        """Retry webhook deliveries.

        Replays up to 100 deliveries. A replay carries the same event `id` as the original, so a
        handler that deduplicates on it stays correct.
        """
        return self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries/retry",
            json=params,
            timeout=timeout,
        )


class Events(SyncResource):
    """Read back what happened in the workspace — the events webhooks carry, whether or not an
    endpoint heard them.
    """

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        type: Sequence[Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]] | None = None,
        email_id: str | None = None,
        timeout: Timeout = None,
    ) -> EventPage:
        """List events.

        Lists the workspace's events, newest first — every event, recorded when it happens,
        whether or not a webhook endpoint subscribes to its type. Each is the envelope a webhook
        delivers, with the same `id`, so a handler that deduplicates on it can read from here and
        from its endpoint alike. Filter by `type`, repeated for any of several, or by `email_id`
        for what happened to one email. To catch up after missed webhooks, walk forward:
        `order=asc` with `after` set to the `created_at` of the last event you processed. `data`
        is the summary every endpoint receives; the `data.email` a `full` endpoint is sent is
        read when a delivery goes out and not kept, so read the email by its `email_id`. Test
        events sent to an endpoint are not listed.
        """
        return self._request(
            "GET",
            "/events",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "type": type,
                "email_id": email_id,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        type: Sequence[Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]] | None = None,
        email_id: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[WebhookEvent]:
        """List events, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                after=after,
                before=before,
                order=order,
                type=type,
                email_id=email_id,
                timeout=timeout,
            )
        )

    def retrieve(
        self,
        event_id: str,
        *,
        timeout: Timeout = None,
    ) -> WebhookEvent:
        """Retrieve an event.

        Returns one event by id — the `id` of the envelope a webhook delivered, which is also the
        `AIInbx-Event-ID` header and a delivery's `event_id`.
        """
        return self._request(
            "GET",
            f"/events/{path_segment(event_id)}",
            timeout=timeout,
        )


class Suppressions(SyncResource):
    """Prevent delivery to opted-out or unsafe recipients."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        key: str | None = None,
        address: str | None = None,
        reason: Literal["complaint", "bounce", "unsubscribe", "manual"] | None = None,
        timeout: Timeout = None,
    ) -> SuppressionPage:
        """List suppressions.

        Lists suppression entries, filterable by list `key`, `reason`, or a substring of the
        `address`. `blocks` and `last_blocked_at` show how often each entry has actually stopped
        a send.
        """
        return self._request(
            "GET",
            "/suppressions",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "key": key,
                "address": address,
                "reason": reason,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        key: str | None = None,
        address: str | None = None,
        reason: Literal["complaint", "bounce", "unsubscribe", "manual"] | None = None,
        timeout: Timeout = None,
    ) -> Iterator[Suppression]:
        """List suppressions, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                key=key,
                address=address,
                reason=reason,
                timeout=timeout,
            )
        )

    def add(
        self,
        params: SuppressionRequest,
        *,
        timeout: Timeout = None,
    ) -> SuppressionBatch:
        """Create suppressions.

        Adds up to 1000 addresses to a suppression list. `key` defaults to the workspace-wide `*`
        list and `scope` to `all`; a `scope` of `optional` blocks only sends marked as
        unsubscribable, so a marketing opt-out does not stop a password reset. Adding an address
        that is already listed updates the existing entry rather than duplicating it, and never
        narrows a wider scope. `space_id` puts the entries on a space's list, which stops that
        space's sends alone; without it they stop every space's.
        """
        return self._request(
            "POST",
            "/suppressions",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> Suppression:
        """Retrieve a suppression.

        Returns one suppression entry, including how it was created and how many sends it has
        stopped.
        """
        return self._request(
            "GET",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )

    def remove(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> SuppressionDeleted:
        """Delete a suppression.

        Removes a suppression entry, allowing sends to that address again. Removing a `bounce` or
        `complaint` entry means mailing an address that already rejected you or reported you as
        spam — do it only with specific evidence the address was fixed. `provider_suppressed`
        says whether SES itself still refuses the address, which removing the entry does not
        change.
        """
        return self._request(
            "DELETE",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )


class PacingRules(SyncResource):
    """Rules that pace outgoing mail: sending hours, and caps per sender, recipient or domain."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> PacingRulePage:
        """List pacing rules.

        Lists the workspace's pacing rules, both sending-hours and rate-limit kinds. Rules with
        `builtin: true` came with the workspace: they cap mail sent from the [provided
        domain](/guides/domains#your-provided-domain) and cannot be changed or removed.
        """
        return self._request(
            "GET",
            "/pacing-rules",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> Iterator[PacingRule]:
        """List pacing rules, every page."""
        yield from iterate_pages(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                timeout=timeout,
            )
        )

    def create(
        self,
        params: PacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> PacingRule:
        """Create a pacing rule.

        Creates a pacing rule. An `hours` rule holds mail outside the weekly windows you declare,
        evaluated in the rule's own timezone. A `limit` rule caps sends per rolling window
        against a scope — the rule as a whole, or per sender address, sending domain, recipient,
        or recipient domain. An empty `match` array applies the rule to every send. `space_id`
        makes the rule read one space's mail alone; workspace rules apply to every space and
        stack on top. An enabled rule counts against the plan's active custom pacing rules: with
        none left the request fails with 402 `allowance_reached`, and a workspace with no plan
        with 402 `plan_required`. A rule created with `enabled` false takes nothing until it is
        switched on.
        """
        return self._request(
            "POST",
            "/pacing-rules",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> PacingRule:
        """Retrieve a pacing rule.

        Returns one pacing rule with its match patterns and its schedule or limit.
        """
        return self._request(
            "GET",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    def update(
        self,
        rule_id: str,
        params: UpdatePacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> PacingRule:
        """Update a pacing rule.

        Updates a pacing rule. At least one field is required. Setting `enabled` to false parks a
        rule without losing its configuration, which is the quickest way to confirm which rule is
        holding mail. A `builtin` rule cannot be changed and fails with `rule_builtin`. Setting
        `enabled` to true on a parked rule takes one of the plan's active custom pacing rules
        again, and fails with 402 `allowance_reached` when none is left.
        """
        return self._request(
            "PATCH",
            f"/pacing-rules/{path_segment(rule_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a pacing rule.

        Deletes a pacing rule. Messages it was holding become eligible to send as soon as the
        remaining rules allow. A `builtin` rule cannot be deleted and fails with `rule_builtin`.
        """
        return self._request(
            "DELETE",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    def retrieve_spread(
        self,
        *,
        timeout: Timeout = None,
    ) -> PacingSpread:
        """Retrieve pacing spread.

        Returns the workspace's send-timing spread, a value from 0 to 100.
        """
        return self._request(
            "GET",
            "/pacing-rules/spread",
            timeout=timeout,
        )

    def update_spread(
        self,
        params: PacingSpreadRequest,
        *,
        timeout: Timeout = None,
    ) -> PacingSpread:
        """Update pacing spread.

        Sets how much randomness is added to send timing. At 0 a rate-limited stream goes out on
        a metronome; higher values vary the gaps, costing a little throughput in exchange for
        traffic that does not look machine-generated. Applies to limit rules.
        """
        return self._request(
            "PATCH",
            "/pacing-rules/spread",
            json=params,
            timeout=timeout,
        )


class Pacing(SyncResource):
    """The mail pacing holds right now, the rule holding each, and releasing it early."""

    def retrieve(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> PacingQueue:
        """Retrieve the pacing queue.

        Returns a snapshot of everything pacing is currently holding: a sample of queued
        messages, the rules in effect, and per-rule counts of how many messages each matched and
        how many it is holding. The per-rule counts are the fastest way to identify which rule is
        responsible.
        """
        return self._request(
            "GET",
            "/pacing-queue",
            params={
                "limit": limit,
                "space": space,
            },
            timeout=timeout,
        )

    def release(
        self,
        params: PacingReleaseRequest,
        *,
        timeout: Timeout = None,
    ) -> IdListResponse:
        """Release emails from the pacing queue.

        Releases up to 500 held emails immediately. `count_toward_limits` defaults to true;
        setting it to false means the sends do not consume rule budget, which makes the rule
        under-count — reserve it for genuinely exceptional releases. For mail that should never
        queue, set `pacing.skip` on the send instead.
        """
        return self._request(
            "POST",
            "/pacing-queue/release",
            json=params,
            timeout=timeout,
        )


class Workspaces(SyncResource):
    """The workspace a request acts in: its name, and the defaults new domains start with."""

    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> WorkspaceList:
        """List workspaces.

        Lists the workspaces the caller can act in, with its role in each. An API key reaches its
        own workspace alone. An OAuth token reaches every workspace it was granted, and a request
        with one that reaches several names the workspace it acts in with the `AIInbx-Workspace`
        header, set to an `id` from here; this list is the one call that needs no header. `mode`
        says whether the caller acts as the whole of its workspaces or as an inbox; a token
        connected as an inbox reaches the workspaces of its inboxes, and `inboxes` names the
        addresses it reads and sends as.
        """
        return self._request(
            "GET",
            "/workspaces",
            timeout=timeout,
        )

    def retrieve(
        self,
        *,
        timeout: Timeout = None,
    ) -> Workspace:
        """Retrieve the workspace.

        Returns the workspace the request acts in: its name, its slug, and the tracking defaults
        a domain added from now on starts with.
        """
        return self._request(
            "GET",
            "/workspace",
            timeout=timeout,
        )

    def update(
        self,
        params: UpdateWorkspaceRequest,
        *,
        timeout: Timeout = None,
    ) -> Workspace:
        """Update the workspace.

        Renames the workspace or changes its tracking defaults; only the fields given change. A
        new name brings a new slug, which moves the console URLs with it (the provided domain
        keeps its name), so a workspace can be renamed once a month — sooner fails with 409
        `rename_cooldown`. Tracking defaults apply to domains added from now on; each existing
        domain keeps its own. Admin only.
        """
        return self._request(
            "PATCH",
            "/workspace",
            json=params,
            timeout=timeout,
        )


class Members(SyncResource):
    """Who is in the workspace and what each of them may do. Admin only."""

    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> MemberList:
        """List members.

        Lists everyone in the workspace, earliest to join first, with their role and when they
        were last active. A workspace holds at most 100 members, so the list is never paged.
        Admin only.
        """
        return self._request(
            "GET",
            "/members",
            timeout=timeout,
        )

    def update(
        self,
        member_id: str,
        params: UpdateMemberRequest,
        *,
        timeout: Timeout = None,
    ) -> Member:
        """Update a member.

        Changes what a member may do: `admin` manages the workspace, its members and its keys;
        `member` works with mail. It takes effect on their next request. The owner's role is not
        changed here — 409 `owner_protected` — the workspace changes hands by a transfer, in the
        console. Admin only.
        """
        return self._request(
            "PATCH",
            f"/members/{path_segment(member_id)}",
            json=params,
            timeout=timeout,
        )

    def remove(
        self,
        member_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Remove a member.

        Takes a member's access away at once. The mail they sent and the API keys they created
        stay with the workspace. The owner cannot be removed (409 `owner_protected`). Admin only.
        """
        return self._request(
            "DELETE",
            f"/members/{path_segment(member_id)}",
            timeout=timeout,
        )


class Invitations(SyncResource):
    """Invitations to join the workspace, waiting to be accepted. Admin only."""

    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> InvitationList:
        """List invitations.

        Lists the invitations nobody has answered, newest first — lapsed ones too, past their
        `expires_at`: those can no longer be accepted, and inviting the address again sends a
        fresh one. Admin only.
        """
        return self._request(
            "GET",
            "/invitations",
            timeout=timeout,
        )

    def create(
        self,
        params: CreateInvitationRequest,
        *,
        timeout: Timeout = None,
    ) -> Invitation:
        """Invite someone.

        Mails an invitation to join the workspace, with a link that is good for seven days.
        Inviting an address that already has one waiting replaces it once the new mail has gone —
        the earlier link then stops working — which is also how an invitation is sent again. An
        address that is already a member fails with 409 `already_member`. When the mail cannot
        go, nothing is created and any earlier invitation keeps working: the address has been
        invited too often today, or the inviter has sent too many, fails with 429
        `invitation_not_sent` — try again later; an address that asked not to hear from us fails
        with 400 `recipients_suppressed`, which will not change on retrying. Invitations sent
        with an API key are in the name of the person who created the key, or the owner once they
        are gone. Admin only.
        """
        return self._request(
            "POST",
            "/invitations",
            json=params,
            timeout=timeout,
        )

    def cancel(
        self,
        invitation_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Cancel an invitation.

        Cancels an invitation that is waiting to be accepted; the link in the mail stops working.
        Send a new one if they still need it. Admin only.
        """
        return self._request(
            "DELETE",
            f"/invitations/{path_segment(invitation_id)}",
            timeout=timeout,
        )


class Attachments(SyncResource):
    """Download original and prepared attachment content."""

    def download(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> bytes:
        """Download an attachment.

        Redirects to a short-lived signed URL for the attachment's original bytes. Follow the
        redirect; the signed URL expires, so resolve it on demand rather than storing it.
        """
        return self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
            binary=True,
        )

    def inspect(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Inspect attachment metadata.

        Returns the attachment's media type, size, and filename disposition in response headers
        without transferring the file — the cheap way to check a size before committing to a
        download.
        """
        return self._request(
            "HEAD",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
        )

    def content(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> str:
        """Download prepared attachment text.

        Redirects to a short-lived signed URL for the attachment's prepared text — Markdown where
        the document has structure, plain text otherwise. Returns 404 `not_prepared` when the
        file type has no text to extract or preparation failed.
        """
        content: bytes = self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}/content",
            timeout=timeout,
            binary=True,
        )
        return content.decode("utf-8")


class RawSpaces(SyncRawResource):
    """Group a workspace's domains, mailboxes and mail by customer. Optional: a workspace that is
    not a platform never needs one.
    """

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        external_id: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SpacePage]:
        """List spaces.

        Lists the workspace's spaces, oldest first. Filter by `external_id` to find the one that
        stands for a customer of yours.
        """
        return self._request(
            "GET",
            "/spaces",
            params={
                "limit": limit,
                "cursor": cursor,
                "external_id": external_id,
            },
            timeout=timeout,
        )

    def create(
        self,
        params: CreateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Space]:
        """Create a space.

        Creates a space — one per customer, typically. Domains, mailboxes, rules and suppressions
        are put in a space with `space_id` when they are created, and every email and thread
        inherits the space of the domain or mailbox it went through. Anything created without a
        `space_id` belongs to the workspace itself and `space_id` reads as null. API keys and
        webhook endpoints belong to the workspace. `external_id` is your own id for the customer:
        unique per workspace, so a second space for the same customer is `409 external_id_taken`,
        and the space can be found by it with `GET /spaces?external_id=`.
        """
        return self._request(
            "POST",
            "/spaces",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Space]:
        """Retrieve a space.

        Returns one space by id, with its name and the `external_id` you gave it.
        """
        return self._request(
            "GET",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )

    def update(
        self,
        space_id: str,
        params: UpdateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Space]:
        """Update a space.

        Changes the space's name or `external_id`; only the fields given change, and
        `external_id: null` clears it. Nothing in the space moves.
        """
        return self._request(
            "PATCH",
            f"/spaces/{path_segment(space_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a space.

        Marks the space for deletion and starts its teardown in the background. The space
        immediately stops accepting work and no longer appears in the API; its domains then come
        off DNS verification and sending, its mailboxes are disconnected, and its emails,
        threads, rules and suppressions are removed. A wildcard domain in the space is deleted
        with its subdomains, including any filed in other spaces. Admin only.
        """
        return self._request(
            "DELETE",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )


class RawApiKeys(SyncRawResource):
    """Create and delete credentials for API access."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[ApiKeyPage]:
        """List API keys.

        Lists the workspace's API keys, newest first. Keys are returned as metadata only — the
        prefix, scope, creation time, and `last_used_at`; the secret itself is never readable
        after creation. Admin only.
        """
        return self._request(
            "GET",
            "/api-keys",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    def create(
        self,
        params: CreateApiKeyRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[ApiKeyCreated]:
        """Create an API key.

        Creates an organization-wide API key and returns its secret exactly once, in the `key`
        field. Store it before the response is discarded — it cannot be recovered. Choose the
        narrowest scope the caller needs: `read`, `sending`, or `full`. The key reaches the whole
        workspace, spaces included. Admin only.
        """
        return self._request(
            "POST",
            "/api-keys",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        key_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete an API key.

        Deletes a key immediately. It authenticates nothing afterwards and cannot be recovered;
        issue a new key instead. Admin only.
        """
        return self._request(
            "DELETE",
            f"/api-keys/{path_segment(key_id)}",
            timeout=timeout,
        )


class RawEmails(SyncRawResource):
    """Send, inspect, and schedule email."""

    def send(
        self,
        params: SendEmailRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SendEmailResponse]:
        """Send an email.

        Sends an email — or, with `draft: true`, writes it for a person to review and send.
        Requires a `from` address on a verified domain or a connected mailbox, and at least one
        of `html` or `text`. `thread_id` continues a conversation; to answer a message AI Inbx
        has not seen — mail from before a migration, or from another provider — name it in
        `in_reply_to` and `references` instead. Recipients on a matching suppression list are
        dropped and reported in `suppressed`; a pacing rule that holds the message is reported in
        `pacing`. Pass `Idempotency-Key` so a retry after a timeout replays the original send
        instead of sending twice. A workspace with no plan fails with 402 `plan_required`, and
        one that has used its plan's emails for the month with 402 `allowance_reached`.
        """
        return self._request(
            "POST",
            "/emails",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        direction: Literal["inbound", "outbound"] | None = None,
        status: Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"] | None = None,
        thread_id: str | None = None,
        query: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[EmailPage]:
        """List emails.

        Lists emails in the workspace, newest first. Filter by `direction`, delivery `status`, a
        single `thread_id`, or a literal `query`: every word in it must appear in the subject,
        the sender, a recipient or the Message-ID, in any order and case. The query is a literal
        filter; the API does not provide semantic email search. To sync, walk forward instead:
        `order=asc` with `after` set to the `created_at` of the last email you have lists only
        what is new, oldest first.
        """
        return self._request(
            "GET",
            "/emails",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "direction": direction,
                "status": status,
                "thread_id": thread_id,
                "query": query,
            },
            timeout=timeout,
        )

    def retrieve(
        self,
        email_id: str,
        *,
        include: Sequence[Literal["attachment_content"]] | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[FullEmail]:
        """Retrieve an email.

        Returns one email in full: both bodies, every header, attachments, the delivery event
        history, and tracked engagements. Pass `include=attachment_content` to inline each
        attachment's prepared text, which saves a request per attachment before handing a message
        to a model.
        """
        return self._request(
            "GET",
            f"/emails/{path_segment(email_id)}",
            params={
                "include": include,
            },
            timeout=timeout,
        )

    def update(
        self,
        email_id: str,
        params: UpdateEmailRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Email]:
        """Update an email.

        Changes an email that has not gone out — a `draft` or a `scheduled` one: its recipients,
        subject, bodies, attachments or send time. Fields left out stay as they are. The email is
        composed again when it goes, so what is sent is what it says by then. One that has begun
        sending, or was canceled or discarded, returns 409 `not_scheduled`.
        """
        return self._request(
            "PATCH",
            f"/emails/{path_segment(email_id)}",
            json=params,
            timeout=timeout,
        )

    def send_draft(
        self,
        email_id: str,
        params: SendDraftRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Email]:
        """Send a draft.

        Sends a draft: at the `scheduled_at` given, else at the draft's own while it is still
        ahead, else now. From here it is a `scheduled` email — counted against the plan, and
        composed again when it goes. Anything but a draft returns 409 `not_draft`; a workspace
        out of emails returns 402.
        """
        return self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/send",
            json=params or {},
            timeout=timeout,
        )

    def cancel(
        self,
        email_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Email]:
        """Cancel an email.

        Cancels a scheduled email before it is composed and sent — its status becomes `canceled`
        — or discards a draft, which becomes `discarded`. Either is terminal: the email cannot be
        put back into flight.
        """
        return self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/cancel",
            timeout=timeout,
        )


class RawThreads(SyncRawResource):
    """Read email conversations."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        query: str | None = None,
        mailbox: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[ThreadPage]:
        """List threads.

        Lists conversations, most recently active first. Every word of `query` must appear in the
        subject, the mailbox or a participant's address, literally and in any order; `mailbox`
        narrows to one address.
        """
        return self._request(
            "GET",
            "/threads",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "query": query,
                "mailbox": mailbox,
            },
            timeout=timeout,
        )

    def retrieve(
        self,
        thread_id: str,
        *,
        message_limit: int | None = None,
        message_cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[FullThread]:
        """Retrieve a thread.

        Returns a thread with its messages inline, oldest first. Messages paginate independently
        of the thread list via `message_limit` and `message_cursor`, so a long conversation can
        be walked without loading it whole.
        """
        return self._request(
            "GET",
            f"/threads/{path_segment(thread_id)}",
            params={
                "message_limit": message_limit,
                "message_cursor": message_cursor,
            },
            timeout=timeout,
        )

    def reply(
        self,
        thread_id: str,
        params: ReplyThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SendEmailResponse]:
        """Reply in a thread.

        Replies within a thread. The sender, recipients, subject, and the `In-Reply-To` and
        `References` headers are inferred from the conversation, as a mail client infers them
        from the email answered: `email_id`, or the thread's latest. The reply follows that
        email's Reply-To; one that names only your own addresses is refused with 400
        `no_recipients` rather than guessed around. Only the content is required — set
        `reply_all` or the individual fields to override what is inferred. Suppression and pacing
        behave exactly as on a send; an `Idempotency-Key` is bound to the request, so a retry
        replays the reply even after the thread has moved on. So does the plan: 402
        `plan_required` without one, 402 `allowance_reached` once its emails are used up.
        """
        return self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/reply",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    def forward(
        self,
        thread_id: str,
        params: ForwardThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SendEmailResponse]:
        """Forward a thread.

        Sends the whole thread as one email to recipients who were not on it. Every message is
        rendered into one transcript, oldest first, each turn as what its author wrote with
        quoted tails and repeated signatures removed; the thread's attachments ride along unless
        `include_attachments` is false, and `note` is placed above the transcript. Only `to` is
        required: the sender defaults to the thread's mailbox and the subject to `Fwd:` and the
        thread's. The forward opens a thread of its own, linked back through `forward_of`, so a
        later reply on the original still goes to its participants and replies to the forward
        land on the forward. Suppression, pacing, scheduling, and idempotency behave exactly as
        on a send. So does the plan: 402 `plan_required` without one, 402 `allowance_reached`
        once its emails are used up.
        """
        return self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/forward",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )


class RawDomains(SyncRawResource):
    """Manage sending domains and DNS checks."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[DomainPage]:
        """List domains.

        Lists the workspace's sending domains with their verification state and tracking
        settings.
        """
        return self._request(
            "GET",
            "/domains",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    def create(
        self,
        params: CreateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Create a domain.

        Registers a sending domain and returns the DNS records to publish: SPF, DKIM, DMARC, a
        return path, and an MX record for receiving. `region` selects the regional mail
        infrastructure for this domain; it can be changed with `PATCH /domains/{domain_id}` until
        the domain is verified.

        A wildcard — `*.acme.dev` — is verified once and covers every subdomain: the MX record
        goes at `*.acme.dev`, the rest at `acme.dev`, and the apex keeps whatever mail setup it
        has. A name one label under a wildcard of yours — `hi.acme.dev` under `*.acme.dev` — is
        created as a subdomain of it: no records, verified as soon as the wildcard is, in
        whatever `space_id` you give it. That is how a platform hands each customer an address of
        their own without touching DNS again.

        A domain name can be connected in several spaces and workspaces, but sending and
        receiving are enabled for the one whose DKIM key is published. To move them, add the
        domain where it should go and publish its DNS records. The next verification check moves
        them; existing mail stays where it was. Duplicate apex or wildcard identities within one
        space fail with `domain_taken`.

        Every workspace already has one domain it did not add: `<slug>.aiinbx.app`, listed with
        `provided: true`. It is verified through our zone, has no records and cannot be deleted;
        a name under `aiinbx.app` cannot be added by hand and fails with `reserved_domain`.

        A domain of its own counts against the plan's custom domains — a subdomain under a
        wildcard and the provided domain do not. With none left the request fails with 402
        `allowance_reached`, and a workspace with no plan with 402 `plan_required`.

        `track_opens` and `track_clicks` set the domain's `tracking`; what they leave out starts
        as the workspace's tracking defaults in the console say — off unless they are set there —
        or, on a subdomain, as its wildcard's. Change either afterwards with `PATCH
        /domains/{domain_id}`.
        """
        return self._request(
            "POST",
            "/domains",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Retrieve a domain.

        Returns one domain with its DNS records and the state of each — `pending`, `verified`, or
        `missing` — along with when each was last checked.
        """
        return self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    def update(
        self,
        domain_id: str,
        params: UpdateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Update domain tracking settings.

        Updates whether opens and clicks are tracked on mail sent from the domain. Applies to
        every send from it that does not say otherwise in `tracking`, from the next one to leave.
        At least one field is required.
        """
        return self._request(
            "PATCH",
            f"/domains/{path_segment(domain_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a domain.

        Deletes a domain and stops future sends from it. Remove the published DNS records
        afterwards. A wildcard's subdomains are deleted with it, in whatever space they sit; a
        subdomain is removed on its own, with nothing to unpublish. The provided domain cannot be
        deleted and fails with `domain_provided`.
        """
        return self._request(
            "DELETE",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    def verify(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Verify domain DNS records now.

        Checks the domain's DNS records against live DNS now. `verified_at` stays null until the
        sending identity’s DKIM verification succeeds; inbound MX, SPF, and DMARC readiness are
        separate. DNS propagation usually takes minutes and occasionally hours, so poll at a sane
        interval or subscribe to the `domain.verified` webhook instead. Domains are also
        rechecked in the background: a verified domain whose DKIM record stops resolving gets
        `dkim_missing_since`, keeps sending, and `domain.at_risk` is sent; `domain.restored`
        follows if the record is back, and has held for an hour, by `stops_sending_at`, otherwise
        it loses `verified_at` and `domain.lost` is sent.
        """
        return self._request(
            "POST",
            f"/domains/{path_segment(domain_id)}/verify",
            timeout=timeout,
        )

    def diagnostics(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[DnsDiagnosticsResponse]:
        """Diagnose domain DNS configuration.

        Reads the domain's live DNS zone and reports what is wrong with it — a duplicate SPF
        record, a permissive policy, a missing return path. Each finding carries a severity, an
        explanation, the fix, and the records it was drawn from. Nothing is stored; the result
        always reflects DNS as it is right now.
        """
        return self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}/diagnostics",
            timeout=timeout,
        )


class RawMailboxes(SyncRawResource):
    """Connect and manage provider mailboxes."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[MailboxPage]:
        """List mailboxes.

        Lists connected Gmail and Outlook mailboxes with their sync state.
        """
        return self._request(
            "GET",
            "/mailboxes",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    def connect(
        self,
        params: ConnectMailboxRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[ConnectMailboxResponse]:
        """Create a mailbox connection URL.

        Creates a single-use, short-lived URL that walks a customer through authorizing their
        Gmail or Outlook mailbox. Redirect them to it rather than emailing it. Pass `ref` — your
        own identifier — and `metadata` for anything else you want kept with the mailbox; both
        are stored on it and carried on every `mailbox.*` webhook. On a reconnect each replaces
        what the mailbox had, and one left out leaves it alone. The `mailbox.connected` webhook —
        not the browser returning to `return_to` — is the authoritative signal that the mailbox
        is live. `return_to` may be any URL here, since the request is authenticated; a connect
        link opened from a browser is held to the app's `return_urls` instead. `space_id` files
        the mailbox in a space; the returned URL carries it, so a platform mints one link per
        customer server-side rather than handing out the bare hosted link. A workspace with no
        plan fails with 402 `plan_required`. A mailbox counts against the plan's mailboxes, but
        which one it will be is only known once the person has authorized: with none left, a
        mailbox the workspace does not already hold is refused then, and the refusal is reported
        in `error` on `return_to`. Reconnecting one that is `active` or `needs_reauth` takes
        nothing new.
        """
        return self._request(
            "POST",
            "/mailboxes/connect",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Mailbox]:
        """Retrieve a mailbox.

        Returns one mailbox, including its `state` and the provider's `state_reason` when there
        is one. A mailbox that is not `active` cannot send.
        """
        return self._request(
            "GET",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    def disconnect(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Mailbox]:
        """Disconnect a mailbox.

        Disconnects a mailbox, stopping sync and dropping its stored credentials. Messages
        already received stay on their threads.
        """
        return self._request(
            "DELETE",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    def sync(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[MailboxSyncResponse]:
        """Queue a mailbox sync.

        Queues a catch-up sync for a mailbox. Mail normally arrives on its own through provider
        push notifications, so this is a repair tool rather than a way to poll. Messages found
        surface as ordinary `email.received` events.
        """
        return self._request(
            "POST",
            f"/mailboxes/{path_segment(mailbox_id)}/sync",
            timeout=timeout,
        )


class RawOauthApps(SyncRawResource):
    """Manage customer-owned Google and Microsoft OAuth apps."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthAppPage]:
        """List OAuth apps.

        Lists the workspace's own Google and Microsoft OAuth apps.
        """
        return self._request(
            "GET",
            "/oauth-apps",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    def create(
        self,
        params: CreateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthApp]:
        """Create an OAuth app.

        Registers your own OAuth app so the mailbox consent screen carries your product's name
        rather than AI Inbx. The response returns the `redirect_uri` to register with the
        provider, a hosted `connect_url`, and — for Google — the `push_endpoint` your own Pub/Sub
        topic should publish to. The `slug` is claimed globally because it forms the connect URL.
        `return_urls` lists the pages of yours a connect link (`connect_url` +
        `/start?return_to=…`) may send a person back to; without one, only the hosted page works.
        """
        return self._request(
            "POST",
            "/oauth-apps",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthApp]:
        """Retrieve an OAuth app.

        Returns one OAuth app. The client secret is never returned.
        """
        return self._request(
            "GET",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )

    def update(
        self,
        app_id: str,
        params: UpdateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthApp]:
        """Update an OAuth app.

        Updates an OAuth app's credentials, branding or return URLs. At least one field is
        required. A rotated secret replaces the old one immediately, so update the provider
        first. `return_urls` replaces the whole list.
        """
        return self._request(
            "PATCH",
            f"/oauth-apps/{path_segment(app_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete an OAuth app.

        Deletes an OAuth app. Mailboxes already connected through it keep working until their
        authorization lapses.
        """
        return self._request(
            "DELETE",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )


class RawWebhookEndpoints(SyncRawResource):
    """Configure event delivery and inspect delivery attempts."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpointPage]:
        """List webhook endpoints.

        Lists the workspace's webhook endpoints with their subscriptions and routing rules.
        """
        return self._request(
            "GET",
            "/webhook-endpoints",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    def create(
        self,
        params: WebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpointCreated]:
        """Create a webhook endpoint.

        Registers an organization-wide endpoint and returns its signing secret exactly once, in
        the `secret` field: no later read shows it again. A secret that was lost, or has leaked,
        is replaced with `POST /webhook-endpoints/{endpoint_id}/rotate-secret`, which keeps the
        old one verifying for a grace period while you deploy the new one. `subscriptions` must
        name at least one event type. Setting `payload` to `full` puts the whole email on
        `email.received` and `email.sent`, as `data.email`, so a handler does not have to fetch
        it. Optional routing rules narrow delivery by sender or recipient: a matching `block`
        rule always wins, and an empty allow list means no opinion. The endpoint receives every
        space's events, each stamped with its `space_id`.
        """
        return self._request(
            "POST",
            "/webhook-endpoints",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpoint]:
        """Retrieve a webhook endpoint.

        Returns one endpoint, including when a rotated previous secret stops being accepted.
        """
        return self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    def update(
        self,
        endpoint_id: str,
        params: UpdateWebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpoint]:
        """Update a webhook endpoint.

        Updates an endpoint's URL, subscriptions, routing rules, payload, or enabled state. At
        least one field is required. A change of `payload` applies from the next delivery
        attempt, retries of earlier events included; a `v1` endpoint cannot be `full`. A disabled
        endpoint receives nothing, and events that occur while it is off are not queued for
        later.
        """
        return self._request(
            "PATCH",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a webhook endpoint.

        Deletes an endpoint. Pending deliveries to it stop.
        """
        return self._request(
            "DELETE",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    def rotate_secret(
        self,
        endpoint_id: str,
        params: RotateWebhookSecretRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookSecretResponse]:
        """Rotate a webhook signing secret.

        Issues a new signing secret and returns it, once — the only way to get a secret after the
        endpoint was created. The previous one keeps verifying for `grace_seconds` (a day by
        default, a week at most): every delivery in that window is signed with both, so a
        deployment can roll over without dropping events, and `previous_secret_expires_at` says
        when the overlap ends. Set the grace period to 0 only when a secret has leaked and the
        exposure matters more than the gap.
        """
        return self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/rotate-secret",
            json=params or {},
            timeout=timeout,
        )

    def test(
        self,
        endpoint_id: str,
        params: WebhookTestRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookTestResponse]:
        """Send a test webhook.

        Delivers a synthetic event to the endpoint and reports what it actually did — status
        code, duration, error, and the first 2 KB of its response. The test event is signed like
        a real one, so it exercises signature verification too. `payload` is sent verbatim and
        does not have to match the real shape for that event type. A test event is about no
        message, so on a `full` endpoint the `data.email` of an `email.received` or `email.sent`
        test is the `email` you put in `payload`, or null.
        """
        return self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/test",
            json=params,
            timeout=timeout,
        )

    def list_deliveries(
        self,
        endpoint_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        state: Literal["pending", "delivered", "failed"] | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookDeliveryPage]:
        """List webhook deliveries.

        Lists deliveries to an endpoint, filterable by state. Each carries the event envelope it
        sends and every attempt made: timestamp, status code, duration, error, and the beginning
        of your response, which is usually what explains a rejection. `body` is what is stored.
        For a `full` endpoint that is the envelope without `data.email`: the email is read from
        the message each time a delivery is sent and is not kept with it. It is null for a `v1`
        endpoint — its legacy body is built from the message at send time, not stored — and for a
        delivery nothing was sent for.
        """
        return self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries",
            params={
                "limit": limit,
                "cursor": cursor,
                "state": state,
            },
            timeout=timeout,
        )

    def retry_deliveries(
        self,
        endpoint_id: str,
        params: RetryDeliveriesRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[IdListResponse]:
        """Retry webhook deliveries.

        Replays up to 100 deliveries. A replay carries the same event `id` as the original, so a
        handler that deduplicates on it stays correct.
        """
        return self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries/retry",
            json=params,
            timeout=timeout,
        )


class RawEvents(SyncRawResource):
    """Read back what happened in the workspace — the events webhooks carry, whether or not an
    endpoint heard them.
    """

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        type: Sequence[Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]] | None = None,
        email_id: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[EventPage]:
        """List events.

        Lists the workspace's events, newest first — every event, recorded when it happens,
        whether or not a webhook endpoint subscribes to its type. Each is the envelope a webhook
        delivers, with the same `id`, so a handler that deduplicates on it can read from here and
        from its endpoint alike. Filter by `type`, repeated for any of several, or by `email_id`
        for what happened to one email. To catch up after missed webhooks, walk forward:
        `order=asc` with `after` set to the `created_at` of the last event you processed. `data`
        is the summary every endpoint receives; the `data.email` a `full` endpoint is sent is
        read when a delivery goes out and not kept, so read the email by its `email_id`. Test
        events sent to an endpoint are not listed.
        """
        return self._request(
            "GET",
            "/events",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "type": type,
                "email_id": email_id,
            },
            timeout=timeout,
        )

    def retrieve(
        self,
        event_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEvent]:
        """Retrieve an event.

        Returns one event by id — the `id` of the envelope a webhook delivered, which is also the
        `AIInbx-Event-ID` header and a delivery's `event_id`.
        """
        return self._request(
            "GET",
            f"/events/{path_segment(event_id)}",
            timeout=timeout,
        )


class RawSuppressions(SyncRawResource):
    """Prevent delivery to opted-out or unsafe recipients."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        key: str | None = None,
        address: str | None = None,
        reason: Literal["complaint", "bounce", "unsubscribe", "manual"] | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SuppressionPage]:
        """List suppressions.

        Lists suppression entries, filterable by list `key`, `reason`, or a substring of the
        `address`. `blocks` and `last_blocked_at` show how often each entry has actually stopped
        a send.
        """
        return self._request(
            "GET",
            "/suppressions",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "key": key,
                "address": address,
                "reason": reason,
            },
            timeout=timeout,
        )

    def add(
        self,
        params: SuppressionRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[SuppressionBatch]:
        """Create suppressions.

        Adds up to 1000 addresses to a suppression list. `key` defaults to the workspace-wide `*`
        list and `scope` to `all`; a `scope` of `optional` blocks only sends marked as
        unsubscribable, so a marketing opt-out does not stop a password reset. Adding an address
        that is already listed updates the existing entry rather than duplicating it, and never
        narrows a wider scope. `space_id` puts the entries on a space's list, which stops that
        space's sends alone; without it they stop every space's.
        """
        return self._request(
            "POST",
            "/suppressions",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Suppression]:
        """Retrieve a suppression.

        Returns one suppression entry, including how it was created and how many sends it has
        stopped.
        """
        return self._request(
            "GET",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )

    def remove(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[SuppressionDeleted]:
        """Delete a suppression.

        Removes a suppression entry, allowing sends to that address again. Removing a `bounce` or
        `complaint` entry means mailing an address that already rejected you or reported you as
        spam — do it only with specific evidence the address was fixed. `provider_suppressed`
        says whether SES itself still refuses the address, which removing the entry does not
        change.
        """
        return self._request(
            "DELETE",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )


class RawPacingRules(SyncRawResource):
    """Rules that pace outgoing mail: sending hours, and caps per sender, recipient or domain."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRulePage]:
        """List pacing rules.

        Lists the workspace's pacing rules, both sending-hours and rate-limit kinds. Rules with
        `builtin: true` came with the workspace: they cap mail sent from the [provided
        domain](/guides/domains#your-provided-domain) and cannot be changed or removed.
        """
        return self._request(
            "GET",
            "/pacing-rules",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    def create(
        self,
        params: PacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRule]:
        """Create a pacing rule.

        Creates a pacing rule. An `hours` rule holds mail outside the weekly windows you declare,
        evaluated in the rule's own timezone. A `limit` rule caps sends per rolling window
        against a scope — the rule as a whole, or per sender address, sending domain, recipient,
        or recipient domain. An empty `match` array applies the rule to every send. `space_id`
        makes the rule read one space's mail alone; workspace rules apply to every space and
        stack on top. An enabled rule counts against the plan's active custom pacing rules: with
        none left the request fails with 402 `allowance_reached`, and a workspace with no plan
        with 402 `plan_required`. A rule created with `enabled` false takes nothing until it is
        switched on.
        """
        return self._request(
            "POST",
            "/pacing-rules",
            json=params,
            timeout=timeout,
        )

    def retrieve(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRule]:
        """Retrieve a pacing rule.

        Returns one pacing rule with its match patterns and its schedule or limit.
        """
        return self._request(
            "GET",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    def update(
        self,
        rule_id: str,
        params: UpdatePacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRule]:
        """Update a pacing rule.

        Updates a pacing rule. At least one field is required. Setting `enabled` to false parks a
        rule without losing its configuration, which is the quickest way to confirm which rule is
        holding mail. A `builtin` rule cannot be changed and fails with `rule_builtin`. Setting
        `enabled` to true on a parked rule takes one of the plan's active custom pacing rules
        again, and fails with 402 `allowance_reached` when none is left.
        """
        return self._request(
            "PATCH",
            f"/pacing-rules/{path_segment(rule_id)}",
            json=params,
            timeout=timeout,
        )

    def delete(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a pacing rule.

        Deletes a pacing rule. Messages it was holding become eligible to send as soon as the
        remaining rules allow. A `builtin` rule cannot be deleted and fails with `rule_builtin`.
        """
        return self._request(
            "DELETE",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    def retrieve_spread(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingSpread]:
        """Retrieve pacing spread.

        Returns the workspace's send-timing spread, a value from 0 to 100.
        """
        return self._request(
            "GET",
            "/pacing-rules/spread",
            timeout=timeout,
        )

    def update_spread(
        self,
        params: PacingSpreadRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingSpread]:
        """Update pacing spread.

        Sets how much randomness is added to send timing. At 0 a rate-limited stream goes out on
        a metronome; higher values vary the gaps, costing a little throughput in exchange for
        traffic that does not look machine-generated. Applies to limit rules.
        """
        return self._request(
            "PATCH",
            "/pacing-rules/spread",
            json=params,
            timeout=timeout,
        )


class RawPacing(SyncRawResource):
    """The mail pacing holds right now, the rule holding each, and releasing it early."""

    def retrieve(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[PacingQueue]:
        """Retrieve the pacing queue.

        Returns a snapshot of everything pacing is currently holding: a sample of queued
        messages, the rules in effect, and per-rule counts of how many messages each matched and
        how many it is holding. The per-rule counts are the fastest way to identify which rule is
        responsible.
        """
        return self._request(
            "GET",
            "/pacing-queue",
            params={
                "limit": limit,
                "space": space,
            },
            timeout=timeout,
        )

    def release(
        self,
        params: PacingReleaseRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[IdListResponse]:
        """Release emails from the pacing queue.

        Releases up to 500 held emails immediately. `count_toward_limits` defaults to true;
        setting it to false means the sends do not consume rule budget, which makes the rule
        under-count — reserve it for genuinely exceptional releases. For mail that should never
        queue, set `pacing.skip` on the send instead.
        """
        return self._request(
            "POST",
            "/pacing-queue/release",
            json=params,
            timeout=timeout,
        )


class RawWorkspaces(SyncRawResource):
    """The workspace a request acts in: its name, and the defaults new domains start with."""

    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WorkspaceList]:
        """List workspaces.

        Lists the workspaces the caller can act in, with its role in each. An API key reaches its
        own workspace alone. An OAuth token reaches every workspace it was granted, and a request
        with one that reaches several names the workspace it acts in with the `AIInbx-Workspace`
        header, set to an `id` from here; this list is the one call that needs no header. `mode`
        says whether the caller acts as the whole of its workspaces or as an inbox; a token
        connected as an inbox reaches the workspaces of its inboxes, and `inboxes` names the
        addresses it reads and sends as.
        """
        return self._request(
            "GET",
            "/workspaces",
            timeout=timeout,
        )

    def retrieve(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Workspace]:
        """Retrieve the workspace.

        Returns the workspace the request acts in: its name, its slug, and the tracking defaults
        a domain added from now on starts with.
        """
        return self._request(
            "GET",
            "/workspace",
            timeout=timeout,
        )

    def update(
        self,
        params: UpdateWorkspaceRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Workspace]:
        """Update the workspace.

        Renames the workspace or changes its tracking defaults; only the fields given change. A
        new name brings a new slug, which moves the console URLs with it (the provided domain
        keeps its name), so a workspace can be renamed once a month — sooner fails with 409
        `rename_cooldown`. Tracking defaults apply to domains added from now on; each existing
        domain keeps its own. Admin only.
        """
        return self._request(
            "PATCH",
            "/workspace",
            json=params,
            timeout=timeout,
        )


class RawMembers(SyncRawResource):
    """Who is in the workspace and what each of them may do. Admin only."""

    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[MemberList]:
        """List members.

        Lists everyone in the workspace, earliest to join first, with their role and when they
        were last active. A workspace holds at most 100 members, so the list is never paged.
        Admin only.
        """
        return self._request(
            "GET",
            "/members",
            timeout=timeout,
        )

    def update(
        self,
        member_id: str,
        params: UpdateMemberRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Member]:
        """Update a member.

        Changes what a member may do: `admin` manages the workspace, its members and its keys;
        `member` works with mail. It takes effect on their next request. The owner's role is not
        changed here — 409 `owner_protected` — the workspace changes hands by a transfer, in the
        console. Admin only.
        """
        return self._request(
            "PATCH",
            f"/members/{path_segment(member_id)}",
            json=params,
            timeout=timeout,
        )

    def remove(
        self,
        member_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Remove a member.

        Takes a member's access away at once. The mail they sent and the API keys they created
        stay with the workspace. The owner cannot be removed (409 `owner_protected`). Admin only.
        """
        return self._request(
            "DELETE",
            f"/members/{path_segment(member_id)}",
            timeout=timeout,
        )


class RawInvitations(SyncRawResource):
    """Invitations to join the workspace, waiting to be accepted. Admin only."""

    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[InvitationList]:
        """List invitations.

        Lists the invitations nobody has answered, newest first — lapsed ones too, past their
        `expires_at`: those can no longer be accepted, and inviting the address again sends a
        fresh one. Admin only.
        """
        return self._request(
            "GET",
            "/invitations",
            timeout=timeout,
        )

    def create(
        self,
        params: CreateInvitationRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Invitation]:
        """Invite someone.

        Mails an invitation to join the workspace, with a link that is good for seven days.
        Inviting an address that already has one waiting replaces it once the new mail has gone —
        the earlier link then stops working — which is also how an invitation is sent again. An
        address that is already a member fails with 409 `already_member`. When the mail cannot
        go, nothing is created and any earlier invitation keeps working: the address has been
        invited too often today, or the inviter has sent too many, fails with 429
        `invitation_not_sent` — try again later; an address that asked not to hear from us fails
        with 400 `recipients_suppressed`, which will not change on retrying. Invitations sent
        with an API key are in the name of the person who created the key, or the owner once they
        are gone. Admin only.
        """
        return self._request(
            "POST",
            "/invitations",
            json=params,
            timeout=timeout,
        )

    def cancel(
        self,
        invitation_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Cancel an invitation.

        Cancels an invitation that is waiting to be accepted; the link in the mail stops working.
        Send a new one if they still need it. Admin only.
        """
        return self._request(
            "DELETE",
            f"/invitations/{path_segment(invitation_id)}",
            timeout=timeout,
        )


class RawAttachments(SyncRawResource):
    """Download original and prepared attachment content."""

    def download(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[bytes]:
        """Download an attachment.

        Redirects to a short-lived signed URL for the attachment's original bytes. Follow the
        redirect; the signed URL expires, so resolve it on demand rather than storing it.
        """
        return self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
            binary=True,
        )

    def inspect(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Inspect attachment metadata.

        Returns the attachment's media type, size, and filename disposition in response headers
        without transferring the file — the cheap way to check a size before committing to a
        download.
        """
        return self._request(
            "HEAD",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
        )

    def content(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[str]:
        """Download prepared attachment text.

        Redirects to a short-lived signed URL for the attachment's prepared text — Markdown where
        the document has structure, plain text otherwise. Returns 404 `not_prepared` when the
        file type has no text to extract or preparation failed.
        """
        return self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}/content",
            timeout=timeout,
            binary=True,
        )


class AsyncSpaces(AsyncResource):
    """Group a workspace's domains, mailboxes and mail by customer. Optional: a workspace that is
    not a platform never needs one.
    """

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        external_id: str | None = None,
        timeout: Timeout = None,
    ) -> SpacePage:
        """List spaces.

        Lists the workspace's spaces, oldest first. Filter by `external_id` to find the one that
        stands for a customer of yours.
        """
        return await self._request(
            "GET",
            "/spaces",
            params={
                "limit": limit,
                "cursor": cursor,
                "external_id": external_id,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        external_id: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[Space]:
        """List spaces, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                external_id=external_id,
                timeout=timeout,
            )
        ):
            yield item

    async def create(
        self,
        params: CreateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> Space:
        """Create a space.

        Creates a space — one per customer, typically. Domains, mailboxes, rules and suppressions
        are put in a space with `space_id` when they are created, and every email and thread
        inherits the space of the domain or mailbox it went through. Anything created without a
        `space_id` belongs to the workspace itself and `space_id` reads as null. API keys and
        webhook endpoints belong to the workspace. `external_id` is your own id for the customer:
        unique per workspace, so a second space for the same customer is `409 external_id_taken`,
        and the space can be found by it with `GET /spaces?external_id=`.
        """
        return await self._request(
            "POST",
            "/spaces",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> Space:
        """Retrieve a space.

        Returns one space by id, with its name and the `external_id` you gave it.
        """
        return await self._request(
            "GET",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        space_id: str,
        params: UpdateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> Space:
        """Update a space.

        Changes the space's name or `external_id`; only the fields given change, and
        `external_id: null` clears it. Nothing in the space moves.
        """
        return await self._request(
            "PATCH",
            f"/spaces/{path_segment(space_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a space.

        Marks the space for deletion and starts its teardown in the background. The space
        immediately stops accepting work and no longer appears in the API; its domains then come
        off DNS verification and sending, its mailboxes are disconnected, and its emails,
        threads, rules and suppressions are removed. A wildcard domain in the space is deleted
        with its subdomains, including any filed in other spaces. Admin only.
        """
        return await self._request(
            "DELETE",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )


class AsyncApiKeys(AsyncResource):
    """Create and delete credentials for API access."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> ApiKeyPage:
        """List API keys.

        Lists the workspace's API keys, newest first. Keys are returned as metadata only — the
        prefix, scope, creation time, and `last_used_at`; the secret itself is never readable
        after creation. Admin only.
        """
        return await self._request(
            "GET",
            "/api-keys",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[ApiKey]:
        """List API keys, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                timeout=timeout,
            )
        ):
            yield item

    async def create(
        self,
        params: CreateApiKeyRequest,
        *,
        timeout: Timeout = None,
    ) -> ApiKeyCreated:
        """Create an API key.

        Creates an organization-wide API key and returns its secret exactly once, in the `key`
        field. Store it before the response is discarded — it cannot be recovered. Choose the
        narrowest scope the caller needs: `read`, `sending`, or `full`. The key reaches the whole
        workspace, spaces included. Admin only.
        """
        return await self._request(
            "POST",
            "/api-keys",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        key_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete an API key.

        Deletes a key immediately. It authenticates nothing afterwards and cannot be recovered;
        issue a new key instead. Admin only.
        """
        return await self._request(
            "DELETE",
            f"/api-keys/{path_segment(key_id)}",
            timeout=timeout,
        )


class AsyncEmails(AsyncResource):
    """Send, inspect, and schedule email."""

    async def send(
        self,
        params: SendEmailRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> SendEmailResponse:
        """Send an email.

        Sends an email — or, with `draft: true`, writes it for a person to review and send.
        Requires a `from` address on a verified domain or a connected mailbox, and at least one
        of `html` or `text`. `thread_id` continues a conversation; to answer a message AI Inbx
        has not seen — mail from before a migration, or from another provider — name it in
        `in_reply_to` and `references` instead. Recipients on a matching suppression list are
        dropped and reported in `suppressed`; a pacing rule that holds the message is reported in
        `pacing`. Pass `Idempotency-Key` so a retry after a timeout replays the original send
        instead of sending twice. A workspace with no plan fails with 402 `plan_required`, and
        one that has used its plan's emails for the month with 402 `allowance_reached`.
        """
        return await self._request(
            "POST",
            "/emails",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        direction: Literal["inbound", "outbound"] | None = None,
        status: Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"] | None = None,
        thread_id: str | None = None,
        query: str | None = None,
        timeout: Timeout = None,
    ) -> EmailPage:
        """List emails.

        Lists emails in the workspace, newest first. Filter by `direction`, delivery `status`, a
        single `thread_id`, or a literal `query`: every word in it must appear in the subject,
        the sender, a recipient or the Message-ID, in any order and case. The query is a literal
        filter; the API does not provide semantic email search. To sync, walk forward instead:
        `order=asc` with `after` set to the `created_at` of the last email you have lists only
        what is new, oldest first.
        """
        return await self._request(
            "GET",
            "/emails",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "direction": direction,
                "status": status,
                "thread_id": thread_id,
                "query": query,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        direction: Literal["inbound", "outbound"] | None = None,
        status: Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"] | None = None,
        thread_id: str | None = None,
        query: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[Email]:
        """List emails, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                after=after,
                before=before,
                order=order,
                direction=direction,
                status=status,
                thread_id=thread_id,
                query=query,
                timeout=timeout,
            )
        ):
            yield item

    async def retrieve(
        self,
        email_id: str,
        *,
        include: Sequence[Literal["attachment_content"]] | None = None,
        timeout: Timeout = None,
    ) -> FullEmail:
        """Retrieve an email.

        Returns one email in full: both bodies, every header, attachments, the delivery event
        history, and tracked engagements. Pass `include=attachment_content` to inline each
        attachment's prepared text, which saves a request per attachment before handing a message
        to a model.
        """
        return await self._request(
            "GET",
            f"/emails/{path_segment(email_id)}",
            params={
                "include": include,
            },
            timeout=timeout,
        )

    async def update(
        self,
        email_id: str,
        params: UpdateEmailRequest,
        *,
        timeout: Timeout = None,
    ) -> Email:
        """Update an email.

        Changes an email that has not gone out — a `draft` or a `scheduled` one: its recipients,
        subject, bodies, attachments or send time. Fields left out stay as they are. The email is
        composed again when it goes, so what is sent is what it says by then. One that has begun
        sending, or was canceled or discarded, returns 409 `not_scheduled`.
        """
        return await self._request(
            "PATCH",
            f"/emails/{path_segment(email_id)}",
            json=params,
            timeout=timeout,
        )

    async def send_draft(
        self,
        email_id: str,
        params: SendDraftRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> Email:
        """Send a draft.

        Sends a draft: at the `scheduled_at` given, else at the draft's own while it is still
        ahead, else now. From here it is a `scheduled` email — counted against the plan, and
        composed again when it goes. Anything but a draft returns 409 `not_draft`; a workspace
        out of emails returns 402.
        """
        return await self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/send",
            json=params or {},
            timeout=timeout,
        )

    async def cancel(
        self,
        email_id: str,
        *,
        timeout: Timeout = None,
    ) -> Email:
        """Cancel an email.

        Cancels a scheduled email before it is composed and sent — its status becomes `canceled`
        — or discards a draft, which becomes `discarded`. Either is terminal: the email cannot be
        put back into flight.
        """
        return await self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/cancel",
            timeout=timeout,
        )


class GeneratedAsyncThreads(AsyncResource):
    """Read email conversations."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        query: str | None = None,
        mailbox: str | None = None,
        timeout: Timeout = None,
    ) -> ThreadPage:
        """List threads.

        Lists conversations, most recently active first. Every word of `query` must appear in the
        subject, the mailbox or a participant's address, literally and in any order; `mailbox`
        narrows to one address.
        """
        return await self._request(
            "GET",
            "/threads",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "query": query,
                "mailbox": mailbox,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        query: str | None = None,
        mailbox: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[Thread]:
        """List threads, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                query=query,
                mailbox=mailbox,
                timeout=timeout,
            )
        ):
            yield item

    async def retrieve(
        self,
        thread_id: str,
        *,
        message_limit: int | None = None,
        message_cursor: str | None = None,
        timeout: Timeout = None,
    ) -> FullThread:
        """Retrieve a thread.

        Returns a thread with its messages inline, oldest first. Messages paginate independently
        of the thread list via `message_limit` and `message_cursor`, so a long conversation can
        be walked without loading it whole.
        """
        return await self._request(
            "GET",
            f"/threads/{path_segment(thread_id)}",
            params={
                "message_limit": message_limit,
                "message_cursor": message_cursor,
            },
            timeout=timeout,
        )

    async def reply(
        self,
        thread_id: str,
        params: ReplyThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> SendEmailResponse:
        """Reply in a thread.

        Replies within a thread. The sender, recipients, subject, and the `In-Reply-To` and
        `References` headers are inferred from the conversation, as a mail client infers them
        from the email answered: `email_id`, or the thread's latest. The reply follows that
        email's Reply-To; one that names only your own addresses is refused with 400
        `no_recipients` rather than guessed around. Only the content is required — set
        `reply_all` or the individual fields to override what is inferred. Suppression and pacing
        behave exactly as on a send; an `Idempotency-Key` is bound to the request, so a retry
        replays the reply even after the thread has moved on. So does the plan: 402
        `plan_required` without one, 402 `allowance_reached` once its emails are used up.
        """
        return await self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/reply",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    async def forward(
        self,
        thread_id: str,
        params: ForwardThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> SendEmailResponse:
        """Forward a thread.

        Sends the whole thread as one email to recipients who were not on it. Every message is
        rendered into one transcript, oldest first, each turn as what its author wrote with
        quoted tails and repeated signatures removed; the thread's attachments ride along unless
        `include_attachments` is false, and `note` is placed above the transcript. Only `to` is
        required: the sender defaults to the thread's mailbox and the subject to `Fwd:` and the
        thread's. The forward opens a thread of its own, linked back through `forward_of`, so a
        later reply on the original still goes to its participants and replies to the forward
        land on the forward. Suppression, pacing, scheduling, and idempotency behave exactly as
        on a send. So does the plan: 402 `plan_required` without one, 402 `allowance_reached`
        once its emails are used up.
        """
        return await self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/forward",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )


class AsyncDomains(AsyncResource):
    """Manage sending domains and DNS checks."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> DomainPage:
        """List domains.

        Lists the workspace's sending domains with their verification state and tracking
        settings.
        """
        return await self._request(
            "GET",
            "/domains",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[Domain]:
        """List domains, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                timeout=timeout,
            )
        ):
            yield item

    async def create(
        self,
        params: CreateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Create a domain.

        Registers a sending domain and returns the DNS records to publish: SPF, DKIM, DMARC, a
        return path, and an MX record for receiving. `region` selects the regional mail
        infrastructure for this domain; it can be changed with `PATCH /domains/{domain_id}` until
        the domain is verified.

        A wildcard — `*.acme.dev` — is verified once and covers every subdomain: the MX record
        goes at `*.acme.dev`, the rest at `acme.dev`, and the apex keeps whatever mail setup it
        has. A name one label under a wildcard of yours — `hi.acme.dev` under `*.acme.dev` — is
        created as a subdomain of it: no records, verified as soon as the wildcard is, in
        whatever `space_id` you give it. That is how a platform hands each customer an address of
        their own without touching DNS again.

        A domain name can be connected in several spaces and workspaces, but sending and
        receiving are enabled for the one whose DKIM key is published. To move them, add the
        domain where it should go and publish its DNS records. The next verification check moves
        them; existing mail stays where it was. Duplicate apex or wildcard identities within one
        space fail with `domain_taken`.

        Every workspace already has one domain it did not add: `<slug>.aiinbx.app`, listed with
        `provided: true`. It is verified through our zone, has no records and cannot be deleted;
        a name under `aiinbx.app` cannot be added by hand and fails with `reserved_domain`.

        A domain of its own counts against the plan's custom domains — a subdomain under a
        wildcard and the provided domain do not. With none left the request fails with 402
        `allowance_reached`, and a workspace with no plan with 402 `plan_required`.

        `track_opens` and `track_clicks` set the domain's `tracking`; what they leave out starts
        as the workspace's tracking defaults in the console say — off unless they are set there —
        or, on a subdomain, as its wildcard's. Change either afterwards with `PATCH
        /domains/{domain_id}`.
        """
        return await self._request(
            "POST",
            "/domains",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Retrieve a domain.

        Returns one domain with its DNS records and the state of each — `pending`, `verified`, or
        `missing` — along with when each was last checked.
        """
        return await self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        domain_id: str,
        params: UpdateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Update domain tracking settings.

        Updates whether opens and clicks are tracked on mail sent from the domain. Applies to
        every send from it that does not say otherwise in `tracking`, from the next one to leave.
        At least one field is required.
        """
        return await self._request(
            "PATCH",
            f"/domains/{path_segment(domain_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a domain.

        Deletes a domain and stops future sends from it. Remove the published DNS records
        afterwards. A wildcard's subdomains are deleted with it, in whatever space they sit; a
        subdomain is removed on its own, with nothing to unpublish. The provided domain cannot be
        deleted and fails with `domain_provided`.
        """
        return await self._request(
            "DELETE",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    async def verify(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> Domain:
        """Verify domain DNS records now.

        Checks the domain's DNS records against live DNS now. `verified_at` stays null until the
        sending identity’s DKIM verification succeeds; inbound MX, SPF, and DMARC readiness are
        separate. DNS propagation usually takes minutes and occasionally hours, so poll at a sane
        interval or subscribe to the `domain.verified` webhook instead. Domains are also
        rechecked in the background: a verified domain whose DKIM record stops resolving gets
        `dkim_missing_since`, keeps sending, and `domain.at_risk` is sent; `domain.restored`
        follows if the record is back, and has held for an hour, by `stops_sending_at`, otherwise
        it loses `verified_at` and `domain.lost` is sent.
        """
        return await self._request(
            "POST",
            f"/domains/{path_segment(domain_id)}/verify",
            timeout=timeout,
        )

    async def diagnostics(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> DnsDiagnosticsResponse:
        """Diagnose domain DNS configuration.

        Reads the domain's live DNS zone and reports what is wrong with it — a duplicate SPF
        record, a permissive policy, a missing return path. Each finding carries a severity, an
        explanation, the fix, and the records it was drawn from. Nothing is stored; the result
        always reflects DNS as it is right now.
        """
        return await self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}/diagnostics",
            timeout=timeout,
        )


class AsyncMailboxes(AsyncResource):
    """Connect and manage provider mailboxes."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> MailboxPage:
        """List mailboxes.

        Lists connected Gmail and Outlook mailboxes with their sync state.
        """
        return await self._request(
            "GET",
            "/mailboxes",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[Mailbox]:
        """List mailboxes, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                timeout=timeout,
            )
        ):
            yield item

    async def connect(
        self,
        params: ConnectMailboxRequest,
        *,
        timeout: Timeout = None,
    ) -> ConnectMailboxResponse:
        """Create a mailbox connection URL.

        Creates a single-use, short-lived URL that walks a customer through authorizing their
        Gmail or Outlook mailbox. Redirect them to it rather than emailing it. Pass `ref` — your
        own identifier — and `metadata` for anything else you want kept with the mailbox; both
        are stored on it and carried on every `mailbox.*` webhook. On a reconnect each replaces
        what the mailbox had, and one left out leaves it alone. The `mailbox.connected` webhook —
        not the browser returning to `return_to` — is the authoritative signal that the mailbox
        is live. `return_to` may be any URL here, since the request is authenticated; a connect
        link opened from a browser is held to the app's `return_urls` instead. `space_id` files
        the mailbox in a space; the returned URL carries it, so a platform mints one link per
        customer server-side rather than handing out the bare hosted link. A workspace with no
        plan fails with 402 `plan_required`. A mailbox counts against the plan's mailboxes, but
        which one it will be is only known once the person has authorized: with none left, a
        mailbox the workspace does not already hold is refused then, and the refusal is reported
        in `error` on `return_to`. Reconnecting one that is `active` or `needs_reauth` takes
        nothing new.
        """
        return await self._request(
            "POST",
            "/mailboxes/connect",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> Mailbox:
        """Retrieve a mailbox.

        Returns one mailbox, including its `state` and the provider's `state_reason` when there
        is one. A mailbox that is not `active` cannot send.
        """
        return await self._request(
            "GET",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    async def disconnect(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> Mailbox:
        """Disconnect a mailbox.

        Disconnects a mailbox, stopping sync and dropping its stored credentials. Messages
        already received stay on their threads.
        """
        return await self._request(
            "DELETE",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    async def sync(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> MailboxSyncResponse:
        """Queue a mailbox sync.

        Queues a catch-up sync for a mailbox. Mail normally arrives on its own through provider
        push notifications, so this is a repair tool rather than a way to poll. Messages found
        surface as ordinary `email.received` events.
        """
        return await self._request(
            "POST",
            f"/mailboxes/{path_segment(mailbox_id)}/sync",
            timeout=timeout,
        )


class AsyncOauthApps(AsyncResource):
    """Manage customer-owned Google and Microsoft OAuth apps."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> OAuthAppPage:
        """List OAuth apps.

        Lists the workspace's own Google and Microsoft OAuth apps.
        """
        return await self._request(
            "GET",
            "/oauth-apps",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[OAuthApp]:
        """List OAuth apps, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                timeout=timeout,
            )
        ):
            yield item

    async def create(
        self,
        params: CreateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> OAuthApp:
        """Create an OAuth app.

        Registers your own OAuth app so the mailbox consent screen carries your product's name
        rather than AI Inbx. The response returns the `redirect_uri` to register with the
        provider, a hosted `connect_url`, and — for Google — the `push_endpoint` your own Pub/Sub
        topic should publish to. The `slug` is claimed globally because it forms the connect URL.
        `return_urls` lists the pages of yours a connect link (`connect_url` +
        `/start?return_to=…`) may send a person back to; without one, only the hosted page works.
        """
        return await self._request(
            "POST",
            "/oauth-apps",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> OAuthApp:
        """Retrieve an OAuth app.

        Returns one OAuth app. The client secret is never returned.
        """
        return await self._request(
            "GET",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        app_id: str,
        params: UpdateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> OAuthApp:
        """Update an OAuth app.

        Updates an OAuth app's credentials, branding or return URLs. At least one field is
        required. A rotated secret replaces the old one immediately, so update the provider
        first. `return_urls` replaces the whole list.
        """
        return await self._request(
            "PATCH",
            f"/oauth-apps/{path_segment(app_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete an OAuth app.

        Deletes an OAuth app. Mailboxes already connected through it keep working until their
        authorization lapses.
        """
        return await self._request(
            "DELETE",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )


class AsyncWebhookEndpoints(AsyncResource):
    """Configure event delivery and inspect delivery attempts."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> WebhookEndpointPage:
        """List webhook endpoints.

        Lists the workspace's webhook endpoints with their subscriptions and routing rules.
        """
        return await self._request(
            "GET",
            "/webhook-endpoints",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[WebhookEndpoint]:
        """List webhook endpoints, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                timeout=timeout,
            )
        ):
            yield item

    async def create(
        self,
        params: WebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> WebhookEndpointCreated:
        """Create a webhook endpoint.

        Registers an organization-wide endpoint and returns its signing secret exactly once, in
        the `secret` field: no later read shows it again. A secret that was lost, or has leaked,
        is replaced with `POST /webhook-endpoints/{endpoint_id}/rotate-secret`, which keeps the
        old one verifying for a grace period while you deploy the new one. `subscriptions` must
        name at least one event type. Setting `payload` to `full` puts the whole email on
        `email.received` and `email.sent`, as `data.email`, so a handler does not have to fetch
        it. Optional routing rules narrow delivery by sender or recipient: a matching `block`
        rule always wins, and an empty allow list means no opinion. The endpoint receives every
        space's events, each stamped with its `space_id`.
        """
        return await self._request(
            "POST",
            "/webhook-endpoints",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> WebhookEndpoint:
        """Retrieve a webhook endpoint.

        Returns one endpoint, including when a rotated previous secret stops being accepted.
        """
        return await self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        endpoint_id: str,
        params: UpdateWebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> WebhookEndpoint:
        """Update a webhook endpoint.

        Updates an endpoint's URL, subscriptions, routing rules, payload, or enabled state. At
        least one field is required. A change of `payload` applies from the next delivery
        attempt, retries of earlier events included; a `v1` endpoint cannot be `full`. A disabled
        endpoint receives nothing, and events that occur while it is off are not queued for
        later.
        """
        return await self._request(
            "PATCH",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a webhook endpoint.

        Deletes an endpoint. Pending deliveries to it stop.
        """
        return await self._request(
            "DELETE",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    async def rotate_secret(
        self,
        endpoint_id: str,
        params: RotateWebhookSecretRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> WebhookSecretResponse:
        """Rotate a webhook signing secret.

        Issues a new signing secret and returns it, once — the only way to get a secret after the
        endpoint was created. The previous one keeps verifying for `grace_seconds` (a day by
        default, a week at most): every delivery in that window is signed with both, so a
        deployment can roll over without dropping events, and `previous_secret_expires_at` says
        when the overlap ends. Set the grace period to 0 only when a secret has leaked and the
        exposure matters more than the gap.
        """
        return await self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/rotate-secret",
            json=params or {},
            timeout=timeout,
        )

    async def test(
        self,
        endpoint_id: str,
        params: WebhookTestRequest,
        *,
        timeout: Timeout = None,
    ) -> WebhookTestResponse:
        """Send a test webhook.

        Delivers a synthetic event to the endpoint and reports what it actually did — status
        code, duration, error, and the first 2 KB of its response. The test event is signed like
        a real one, so it exercises signature verification too. `payload` is sent verbatim and
        does not have to match the real shape for that event type. A test event is about no
        message, so on a `full` endpoint the `data.email` of an `email.received` or `email.sent`
        test is the `email` you put in `payload`, or null.
        """
        return await self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/test",
            json=params,
            timeout=timeout,
        )

    async def list_deliveries(
        self,
        endpoint_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        state: Literal["pending", "delivered", "failed"] | None = None,
        timeout: Timeout = None,
    ) -> WebhookDeliveryPage:
        """List webhook deliveries.

        Lists deliveries to an endpoint, filterable by state. Each carries the event envelope it
        sends and every attempt made: timestamp, status code, duration, error, and the beginning
        of your response, which is usually what explains a rejection. `body` is what is stored.
        For a `full` endpoint that is the envelope without `data.email`: the email is read from
        the message each time a delivery is sent and is not kept with it. It is null for a `v1`
        endpoint — its legacy body is built from the message at send time, not stored — and for a
        delivery nothing was sent for.
        """
        return await self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries",
            params={
                "limit": limit,
                "cursor": cursor,
                "state": state,
            },
            timeout=timeout,
        )

    async def iter_deliveries(
        self,
        endpoint_id: str,
        *,
        limit: int | None = None,
        state: Literal["pending", "delivered", "failed"] | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[WebhookDelivery]:
        """List webhook deliveries, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list_deliveries(
                endpoint_id,
                cursor=cursor,
                limit=limit,
                state=state,
                timeout=timeout,
            )
        ):
            yield item

    async def retry_deliveries(
        self,
        endpoint_id: str,
        params: RetryDeliveriesRequest,
        *,
        timeout: Timeout = None,
    ) -> IdListResponse:
        """Retry webhook deliveries.

        Replays up to 100 deliveries. A replay carries the same event `id` as the original, so a
        handler that deduplicates on it stays correct.
        """
        return await self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries/retry",
            json=params,
            timeout=timeout,
        )


class AsyncEvents(AsyncResource):
    """Read back what happened in the workspace — the events webhooks carry, whether or not an
    endpoint heard them.
    """

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        type: Sequence[Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]] | None = None,
        email_id: str | None = None,
        timeout: Timeout = None,
    ) -> EventPage:
        """List events.

        Lists the workspace's events, newest first — every event, recorded when it happens,
        whether or not a webhook endpoint subscribes to its type. Each is the envelope a webhook
        delivers, with the same `id`, so a handler that deduplicates on it can read from here and
        from its endpoint alike. Filter by `type`, repeated for any of several, or by `email_id`
        for what happened to one email. To catch up after missed webhooks, walk forward:
        `order=asc` with `after` set to the `created_at` of the last event you processed. `data`
        is the summary every endpoint receives; the `data.email` a `full` endpoint is sent is
        read when a delivery goes out and not kept, so read the email by its `email_id`. Test
        events sent to an endpoint are not listed.
        """
        return await self._request(
            "GET",
            "/events",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "type": type,
                "email_id": email_id,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        type: Sequence[Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]] | None = None,
        email_id: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[WebhookEvent]:
        """List events, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                after=after,
                before=before,
                order=order,
                type=type,
                email_id=email_id,
                timeout=timeout,
            )
        ):
            yield item

    async def retrieve(
        self,
        event_id: str,
        *,
        timeout: Timeout = None,
    ) -> WebhookEvent:
        """Retrieve an event.

        Returns one event by id — the `id` of the envelope a webhook delivered, which is also the
        `AIInbx-Event-ID` header and a delivery's `event_id`.
        """
        return await self._request(
            "GET",
            f"/events/{path_segment(event_id)}",
            timeout=timeout,
        )


class AsyncSuppressions(AsyncResource):
    """Prevent delivery to opted-out or unsafe recipients."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        key: str | None = None,
        address: str | None = None,
        reason: Literal["complaint", "bounce", "unsubscribe", "manual"] | None = None,
        timeout: Timeout = None,
    ) -> SuppressionPage:
        """List suppressions.

        Lists suppression entries, filterable by list `key`, `reason`, or a substring of the
        `address`. `blocks` and `last_blocked_at` show how often each entry has actually stopped
        a send.
        """
        return await self._request(
            "GET",
            "/suppressions",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "key": key,
                "address": address,
                "reason": reason,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        key: str | None = None,
        address: str | None = None,
        reason: Literal["complaint", "bounce", "unsubscribe", "manual"] | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[Suppression]:
        """List suppressions, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                key=key,
                address=address,
                reason=reason,
                timeout=timeout,
            )
        ):
            yield item

    async def add(
        self,
        params: SuppressionRequest,
        *,
        timeout: Timeout = None,
    ) -> SuppressionBatch:
        """Create suppressions.

        Adds up to 1000 addresses to a suppression list. `key` defaults to the workspace-wide `*`
        list and `scope` to `all`; a `scope` of `optional` blocks only sends marked as
        unsubscribable, so a marketing opt-out does not stop a password reset. Adding an address
        that is already listed updates the existing entry rather than duplicating it, and never
        narrows a wider scope. `space_id` puts the entries on a space's list, which stops that
        space's sends alone; without it they stop every space's.
        """
        return await self._request(
            "POST",
            "/suppressions",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> Suppression:
        """Retrieve a suppression.

        Returns one suppression entry, including how it was created and how many sends it has
        stopped.
        """
        return await self._request(
            "GET",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )

    async def remove(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> SuppressionDeleted:
        """Delete a suppression.

        Removes a suppression entry, allowing sends to that address again. Removing a `bounce` or
        `complaint` entry means mailing an address that already rejected you or reported you as
        spam — do it only with specific evidence the address was fixed. `provider_suppressed`
        says whether SES itself still refuses the address, which removing the entry does not
        change.
        """
        return await self._request(
            "DELETE",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )


class AsyncPacingRules(AsyncResource):
    """Rules that pace outgoing mail: sending hours, and caps per sender, recipient or domain."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> PacingRulePage:
        """List pacing rules.

        Lists the workspace's pacing rules, both sending-hours and rate-limit kinds. Rules with
        `builtin: true` came with the workspace: they cap mail sent from the [provided
        domain](/guides/domains#your-provided-domain) and cannot be changed or removed.
        """
        return await self._request(
            "GET",
            "/pacing-rules",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    async def iter(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[PacingRule]:
        """List pacing rules, every page."""
        async for item in iterate_pages_async(
            lambda cursor: self.list(
                cursor=cursor,
                limit=limit,
                space=space,
                timeout=timeout,
            )
        ):
            yield item

    async def create(
        self,
        params: PacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> PacingRule:
        """Create a pacing rule.

        Creates a pacing rule. An `hours` rule holds mail outside the weekly windows you declare,
        evaluated in the rule's own timezone. A `limit` rule caps sends per rolling window
        against a scope — the rule as a whole, or per sender address, sending domain, recipient,
        or recipient domain. An empty `match` array applies the rule to every send. `space_id`
        makes the rule read one space's mail alone; workspace rules apply to every space and
        stack on top. An enabled rule counts against the plan's active custom pacing rules: with
        none left the request fails with 402 `allowance_reached`, and a workspace with no plan
        with 402 `plan_required`. A rule created with `enabled` false takes nothing until it is
        switched on.
        """
        return await self._request(
            "POST",
            "/pacing-rules",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> PacingRule:
        """Retrieve a pacing rule.

        Returns one pacing rule with its match patterns and its schedule or limit.
        """
        return await self._request(
            "GET",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        rule_id: str,
        params: UpdatePacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> PacingRule:
        """Update a pacing rule.

        Updates a pacing rule. At least one field is required. Setting `enabled` to false parks a
        rule without losing its configuration, which is the quickest way to confirm which rule is
        holding mail. A `builtin` rule cannot be changed and fails with `rule_builtin`. Setting
        `enabled` to true on a parked rule takes one of the plan's active custom pacing rules
        again, and fails with 402 `allowance_reached` when none is left.
        """
        return await self._request(
            "PATCH",
            f"/pacing-rules/{path_segment(rule_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Delete a pacing rule.

        Deletes a pacing rule. Messages it was holding become eligible to send as soon as the
        remaining rules allow. A `builtin` rule cannot be deleted and fails with `rule_builtin`.
        """
        return await self._request(
            "DELETE",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    async def retrieve_spread(
        self,
        *,
        timeout: Timeout = None,
    ) -> PacingSpread:
        """Retrieve pacing spread.

        Returns the workspace's send-timing spread, a value from 0 to 100.
        """
        return await self._request(
            "GET",
            "/pacing-rules/spread",
            timeout=timeout,
        )

    async def update_spread(
        self,
        params: PacingSpreadRequest,
        *,
        timeout: Timeout = None,
    ) -> PacingSpread:
        """Update pacing spread.

        Sets how much randomness is added to send timing. At 0 a rate-limited stream goes out on
        a metronome; higher values vary the gaps, costing a little throughput in exchange for
        traffic that does not look machine-generated. Applies to limit rules.
        """
        return await self._request(
            "PATCH",
            "/pacing-rules/spread",
            json=params,
            timeout=timeout,
        )


class AsyncPacing(AsyncResource):
    """The mail pacing holds right now, the rule holding each, and releasing it early."""

    async def retrieve(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> PacingQueue:
        """Retrieve the pacing queue.

        Returns a snapshot of everything pacing is currently holding: a sample of queued
        messages, the rules in effect, and per-rule counts of how many messages each matched and
        how many it is holding. The per-rule counts are the fastest way to identify which rule is
        responsible.
        """
        return await self._request(
            "GET",
            "/pacing-queue",
            params={
                "limit": limit,
                "space": space,
            },
            timeout=timeout,
        )

    async def release(
        self,
        params: PacingReleaseRequest,
        *,
        timeout: Timeout = None,
    ) -> IdListResponse:
        """Release emails from the pacing queue.

        Releases up to 500 held emails immediately. `count_toward_limits` defaults to true;
        setting it to false means the sends do not consume rule budget, which makes the rule
        under-count — reserve it for genuinely exceptional releases. For mail that should never
        queue, set `pacing.skip` on the send instead.
        """
        return await self._request(
            "POST",
            "/pacing-queue/release",
            json=params,
            timeout=timeout,
        )


class AsyncWorkspaces(AsyncResource):
    """The workspace a request acts in: its name, and the defaults new domains start with."""

    async def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> WorkspaceList:
        """List workspaces.

        Lists the workspaces the caller can act in, with its role in each. An API key reaches its
        own workspace alone. An OAuth token reaches every workspace it was granted, and a request
        with one that reaches several names the workspace it acts in with the `AIInbx-Workspace`
        header, set to an `id` from here; this list is the one call that needs no header. `mode`
        says whether the caller acts as the whole of its workspaces or as an inbox; a token
        connected as an inbox reaches the workspaces of its inboxes, and `inboxes` names the
        addresses it reads and sends as.
        """
        return await self._request(
            "GET",
            "/workspaces",
            timeout=timeout,
        )

    async def retrieve(
        self,
        *,
        timeout: Timeout = None,
    ) -> Workspace:
        """Retrieve the workspace.

        Returns the workspace the request acts in: its name, its slug, and the tracking defaults
        a domain added from now on starts with.
        """
        return await self._request(
            "GET",
            "/workspace",
            timeout=timeout,
        )

    async def update(
        self,
        params: UpdateWorkspaceRequest,
        *,
        timeout: Timeout = None,
    ) -> Workspace:
        """Update the workspace.

        Renames the workspace or changes its tracking defaults; only the fields given change. A
        new name brings a new slug, which moves the console URLs with it (the provided domain
        keeps its name), so a workspace can be renamed once a month — sooner fails with 409
        `rename_cooldown`. Tracking defaults apply to domains added from now on; each existing
        domain keeps its own. Admin only.
        """
        return await self._request(
            "PATCH",
            "/workspace",
            json=params,
            timeout=timeout,
        )


class AsyncMembers(AsyncResource):
    """Who is in the workspace and what each of them may do. Admin only."""

    async def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> MemberList:
        """List members.

        Lists everyone in the workspace, earliest to join first, with their role and when they
        were last active. A workspace holds at most 100 members, so the list is never paged.
        Admin only.
        """
        return await self._request(
            "GET",
            "/members",
            timeout=timeout,
        )

    async def update(
        self,
        member_id: str,
        params: UpdateMemberRequest,
        *,
        timeout: Timeout = None,
    ) -> Member:
        """Update a member.

        Changes what a member may do: `admin` manages the workspace, its members and its keys;
        `member` works with mail. It takes effect on their next request. The owner's role is not
        changed here — 409 `owner_protected` — the workspace changes hands by a transfer, in the
        console. Admin only.
        """
        return await self._request(
            "PATCH",
            f"/members/{path_segment(member_id)}",
            json=params,
            timeout=timeout,
        )

    async def remove(
        self,
        member_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Remove a member.

        Takes a member's access away at once. The mail they sent and the API keys they created
        stay with the workspace. The owner cannot be removed (409 `owner_protected`). Admin only.
        """
        return await self._request(
            "DELETE",
            f"/members/{path_segment(member_id)}",
            timeout=timeout,
        )


class AsyncInvitations(AsyncResource):
    """Invitations to join the workspace, waiting to be accepted. Admin only."""

    async def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> InvitationList:
        """List invitations.

        Lists the invitations nobody has answered, newest first — lapsed ones too, past their
        `expires_at`: those can no longer be accepted, and inviting the address again sends a
        fresh one. Admin only.
        """
        return await self._request(
            "GET",
            "/invitations",
            timeout=timeout,
        )

    async def create(
        self,
        params: CreateInvitationRequest,
        *,
        timeout: Timeout = None,
    ) -> Invitation:
        """Invite someone.

        Mails an invitation to join the workspace, with a link that is good for seven days.
        Inviting an address that already has one waiting replaces it once the new mail has gone —
        the earlier link then stops working — which is also how an invitation is sent again. An
        address that is already a member fails with 409 `already_member`. When the mail cannot
        go, nothing is created and any earlier invitation keeps working: the address has been
        invited too often today, or the inviter has sent too many, fails with 429
        `invitation_not_sent` — try again later; an address that asked not to hear from us fails
        with 400 `recipients_suppressed`, which will not change on retrying. Invitations sent
        with an API key are in the name of the person who created the key, or the owner once they
        are gone. Admin only.
        """
        return await self._request(
            "POST",
            "/invitations",
            json=params,
            timeout=timeout,
        )

    async def cancel(
        self,
        invitation_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Cancel an invitation.

        Cancels an invitation that is waiting to be accepted; the link in the mail stops working.
        Send a new one if they still need it. Admin only.
        """
        return await self._request(
            "DELETE",
            f"/invitations/{path_segment(invitation_id)}",
            timeout=timeout,
        )


class AsyncAttachments(AsyncResource):
    """Download original and prepared attachment content."""

    async def download(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> bytes:
        """Download an attachment.

        Redirects to a short-lived signed URL for the attachment's original bytes. Follow the
        redirect; the signed URL expires, so resolve it on demand rather than storing it.
        """
        return await self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
            binary=True,
        )

    async def inspect(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> None:
        """Inspect attachment metadata.

        Returns the attachment's media type, size, and filename disposition in response headers
        without transferring the file — the cheap way to check a size before committing to a
        download.
        """
        return await self._request(
            "HEAD",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
        )

    async def content(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> str:
        """Download prepared attachment text.

        Redirects to a short-lived signed URL for the attachment's prepared text — Markdown where
        the document has structure, plain text otherwise. Returns 404 `not_prepared` when the
        file type has no text to extract or preparation failed.
        """
        content: bytes = await self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}/content",
            timeout=timeout,
            binary=True,
        )
        return content.decode("utf-8")


class AsyncRawSpaces(AsyncRawResource):
    """Group a workspace's domains, mailboxes and mail by customer. Optional: a workspace that is
    not a platform never needs one.
    """

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        external_id: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SpacePage]:
        """List spaces.

        Lists the workspace's spaces, oldest first. Filter by `external_id` to find the one that
        stands for a customer of yours.
        """
        return await self._request(
            "GET",
            "/spaces",
            params={
                "limit": limit,
                "cursor": cursor,
                "external_id": external_id,
            },
            timeout=timeout,
        )

    async def create(
        self,
        params: CreateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Space]:
        """Create a space.

        Creates a space — one per customer, typically. Domains, mailboxes, rules and suppressions
        are put in a space with `space_id` when they are created, and every email and thread
        inherits the space of the domain or mailbox it went through. Anything created without a
        `space_id` belongs to the workspace itself and `space_id` reads as null. API keys and
        webhook endpoints belong to the workspace. `external_id` is your own id for the customer:
        unique per workspace, so a second space for the same customer is `409 external_id_taken`,
        and the space can be found by it with `GET /spaces?external_id=`.
        """
        return await self._request(
            "POST",
            "/spaces",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Space]:
        """Retrieve a space.

        Returns one space by id, with its name and the `external_id` you gave it.
        """
        return await self._request(
            "GET",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        space_id: str,
        params: UpdateSpaceRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Space]:
        """Update a space.

        Changes the space's name or `external_id`; only the fields given change, and
        `external_id: null` clears it. Nothing in the space moves.
        """
        return await self._request(
            "PATCH",
            f"/spaces/{path_segment(space_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        space_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a space.

        Marks the space for deletion and starts its teardown in the background. The space
        immediately stops accepting work and no longer appears in the API; its domains then come
        off DNS verification and sending, its mailboxes are disconnected, and its emails,
        threads, rules and suppressions are removed. A wildcard domain in the space is deleted
        with its subdomains, including any filed in other spaces. Admin only.
        """
        return await self._request(
            "DELETE",
            f"/spaces/{path_segment(space_id)}",
            timeout=timeout,
        )


class AsyncRawApiKeys(AsyncRawResource):
    """Create and delete credentials for API access."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[ApiKeyPage]:
        """List API keys.

        Lists the workspace's API keys, newest first. Keys are returned as metadata only — the
        prefix, scope, creation time, and `last_used_at`; the secret itself is never readable
        after creation. Admin only.
        """
        return await self._request(
            "GET",
            "/api-keys",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    async def create(
        self,
        params: CreateApiKeyRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[ApiKeyCreated]:
        """Create an API key.

        Creates an organization-wide API key and returns its secret exactly once, in the `key`
        field. Store it before the response is discarded — it cannot be recovered. Choose the
        narrowest scope the caller needs: `read`, `sending`, or `full`. The key reaches the whole
        workspace, spaces included. Admin only.
        """
        return await self._request(
            "POST",
            "/api-keys",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        key_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete an API key.

        Deletes a key immediately. It authenticates nothing afterwards and cannot be recovered;
        issue a new key instead. Admin only.
        """
        return await self._request(
            "DELETE",
            f"/api-keys/{path_segment(key_id)}",
            timeout=timeout,
        )


class AsyncRawEmails(AsyncRawResource):
    """Send, inspect, and schedule email."""

    async def send(
        self,
        params: SendEmailRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SendEmailResponse]:
        """Send an email.

        Sends an email — or, with `draft: true`, writes it for a person to review and send.
        Requires a `from` address on a verified domain or a connected mailbox, and at least one
        of `html` or `text`. `thread_id` continues a conversation; to answer a message AI Inbx
        has not seen — mail from before a migration, or from another provider — name it in
        `in_reply_to` and `references` instead. Recipients on a matching suppression list are
        dropped and reported in `suppressed`; a pacing rule that holds the message is reported in
        `pacing`. Pass `Idempotency-Key` so a retry after a timeout replays the original send
        instead of sending twice. A workspace with no plan fails with 402 `plan_required`, and
        one that has used its plan's emails for the month with 402 `allowance_reached`.
        """
        return await self._request(
            "POST",
            "/emails",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        direction: Literal["inbound", "outbound"] | None = None,
        status: Literal["draft", "scheduled", "canceled", "discarded", "queued", "sending", "sent", "delivered", "bounced", "complained", "failed", "received"] | None = None,
        thread_id: str | None = None,
        query: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[EmailPage]:
        """List emails.

        Lists emails in the workspace, newest first. Filter by `direction`, delivery `status`, a
        single `thread_id`, or a literal `query`: every word in it must appear in the subject,
        the sender, a recipient or the Message-ID, in any order and case. The query is a literal
        filter; the API does not provide semantic email search. To sync, walk forward instead:
        `order=asc` with `after` set to the `created_at` of the last email you have lists only
        what is new, oldest first.
        """
        return await self._request(
            "GET",
            "/emails",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "direction": direction,
                "status": status,
                "thread_id": thread_id,
                "query": query,
            },
            timeout=timeout,
        )

    async def retrieve(
        self,
        email_id: str,
        *,
        include: Sequence[Literal["attachment_content"]] | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[FullEmail]:
        """Retrieve an email.

        Returns one email in full: both bodies, every header, attachments, the delivery event
        history, and tracked engagements. Pass `include=attachment_content` to inline each
        attachment's prepared text, which saves a request per attachment before handing a message
        to a model.
        """
        return await self._request(
            "GET",
            f"/emails/{path_segment(email_id)}",
            params={
                "include": include,
            },
            timeout=timeout,
        )

    async def update(
        self,
        email_id: str,
        params: UpdateEmailRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Email]:
        """Update an email.

        Changes an email that has not gone out — a `draft` or a `scheduled` one: its recipients,
        subject, bodies, attachments or send time. Fields left out stay as they are. The email is
        composed again when it goes, so what is sent is what it says by then. One that has begun
        sending, or was canceled or discarded, returns 409 `not_scheduled`.
        """
        return await self._request(
            "PATCH",
            f"/emails/{path_segment(email_id)}",
            json=params,
            timeout=timeout,
        )

    async def send_draft(
        self,
        email_id: str,
        params: SendDraftRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Email]:
        """Send a draft.

        Sends a draft: at the `scheduled_at` given, else at the draft's own while it is still
        ahead, else now. From here it is a `scheduled` email — counted against the plan, and
        composed again when it goes. Anything but a draft returns 409 `not_draft`; a workspace
        out of emails returns 402.
        """
        return await self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/send",
            json=params or {},
            timeout=timeout,
        )

    async def cancel(
        self,
        email_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Email]:
        """Cancel an email.

        Cancels a scheduled email before it is composed and sent — its status becomes `canceled`
        — or discards a draft, which becomes `discarded`. Either is terminal: the email cannot be
        put back into flight.
        """
        return await self._request(
            "POST",
            f"/emails/{path_segment(email_id)}/cancel",
            timeout=timeout,
        )


class AsyncRawThreads(AsyncRawResource):
    """Read email conversations."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        query: str | None = None,
        mailbox: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[ThreadPage]:
        """List threads.

        Lists conversations, most recently active first. Every word of `query` must appear in the
        subject, the mailbox or a participant's address, literally and in any order; `mailbox`
        narrows to one address.
        """
        return await self._request(
            "GET",
            "/threads",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "query": query,
                "mailbox": mailbox,
            },
            timeout=timeout,
        )

    async def retrieve(
        self,
        thread_id: str,
        *,
        message_limit: int | None = None,
        message_cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[FullThread]:
        """Retrieve a thread.

        Returns a thread with its messages inline, oldest first. Messages paginate independently
        of the thread list via `message_limit` and `message_cursor`, so a long conversation can
        be walked without loading it whole.
        """
        return await self._request(
            "GET",
            f"/threads/{path_segment(thread_id)}",
            params={
                "message_limit": message_limit,
                "message_cursor": message_cursor,
            },
            timeout=timeout,
        )

    async def reply(
        self,
        thread_id: str,
        params: ReplyThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SendEmailResponse]:
        """Reply in a thread.

        Replies within a thread. The sender, recipients, subject, and the `In-Reply-To` and
        `References` headers are inferred from the conversation, as a mail client infers them
        from the email answered: `email_id`, or the thread's latest. The reply follows that
        email's Reply-To; one that names only your own addresses is refused with 400
        `no_recipients` rather than guessed around. Only the content is required — set
        `reply_all` or the individual fields to override what is inferred. Suppression and pacing
        behave exactly as on a send; an `Idempotency-Key` is bound to the request, so a retry
        replays the reply even after the thread has moved on. So does the plan: 402
        `plan_required` without one, 402 `allowance_reached` once its emails are used up.
        """
        return await self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/reply",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )

    async def forward(
        self,
        thread_id: str,
        params: ForwardThreadRequest,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SendEmailResponse]:
        """Forward a thread.

        Sends the whole thread as one email to recipients who were not on it. Every message is
        rendered into one transcript, oldest first, each turn as what its author wrote with
        quoted tails and repeated signatures removed; the thread's attachments ride along unless
        `include_attachments` is false, and `note` is placed above the transcript. Only `to` is
        required: the sender defaults to the thread's mailbox and the subject to `Fwd:` and the
        thread's. The forward opens a thread of its own, linked back through `forward_of`, so a
        later reply on the original still goes to its participants and replies to the forward
        land on the forward. Suppression, pacing, scheduling, and idempotency behave exactly as
        on a send. So does the plan: 402 `plan_required` without one, 402 `allowance_reached`
        once its emails are used up.
        """
        return await self._request(
            "POST",
            f"/threads/{path_segment(thread_id)}/forward",
            json=wire(params),
            headers=idempotency_headers(idempotency_key),
            timeout=timeout,
        )


class AsyncRawDomains(AsyncRawResource):
    """Manage sending domains and DNS checks."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[DomainPage]:
        """List domains.

        Lists the workspace's sending domains with their verification state and tracking
        settings.
        """
        return await self._request(
            "GET",
            "/domains",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    async def create(
        self,
        params: CreateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Create a domain.

        Registers a sending domain and returns the DNS records to publish: SPF, DKIM, DMARC, a
        return path, and an MX record for receiving. `region` selects the regional mail
        infrastructure for this domain; it can be changed with `PATCH /domains/{domain_id}` until
        the domain is verified.

        A wildcard — `*.acme.dev` — is verified once and covers every subdomain: the MX record
        goes at `*.acme.dev`, the rest at `acme.dev`, and the apex keeps whatever mail setup it
        has. A name one label under a wildcard of yours — `hi.acme.dev` under `*.acme.dev` — is
        created as a subdomain of it: no records, verified as soon as the wildcard is, in
        whatever `space_id` you give it. That is how a platform hands each customer an address of
        their own without touching DNS again.

        A domain name can be connected in several spaces and workspaces, but sending and
        receiving are enabled for the one whose DKIM key is published. To move them, add the
        domain where it should go and publish its DNS records. The next verification check moves
        them; existing mail stays where it was. Duplicate apex or wildcard identities within one
        space fail with `domain_taken`.

        Every workspace already has one domain it did not add: `<slug>.aiinbx.app`, listed with
        `provided: true`. It is verified through our zone, has no records and cannot be deleted;
        a name under `aiinbx.app` cannot be added by hand and fails with `reserved_domain`.

        A domain of its own counts against the plan's custom domains — a subdomain under a
        wildcard and the provided domain do not. With none left the request fails with 402
        `allowance_reached`, and a workspace with no plan with 402 `plan_required`.

        `track_opens` and `track_clicks` set the domain's `tracking`; what they leave out starts
        as the workspace's tracking defaults in the console say — off unless they are set there —
        or, on a subdomain, as its wildcard's. Change either afterwards with `PATCH
        /domains/{domain_id}`.
        """
        return await self._request(
            "POST",
            "/domains",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Retrieve a domain.

        Returns one domain with its DNS records and the state of each — `pending`, `verified`, or
        `missing` — along with when each was last checked.
        """
        return await self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        domain_id: str,
        params: UpdateDomainRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Update domain tracking settings.

        Updates whether opens and clicks are tracked on mail sent from the domain. Applies to
        every send from it that does not say otherwise in `tracking`, from the next one to leave.
        At least one field is required.
        """
        return await self._request(
            "PATCH",
            f"/domains/{path_segment(domain_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a domain.

        Deletes a domain and stops future sends from it. Remove the published DNS records
        afterwards. A wildcard's subdomains are deleted with it, in whatever space they sit; a
        subdomain is removed on its own, with nothing to unpublish. The provided domain cannot be
        deleted and fails with `domain_provided`.
        """
        return await self._request(
            "DELETE",
            f"/domains/{path_segment(domain_id)}",
            timeout=timeout,
        )

    async def verify(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Domain]:
        """Verify domain DNS records now.

        Checks the domain's DNS records against live DNS now. `verified_at` stays null until the
        sending identity’s DKIM verification succeeds; inbound MX, SPF, and DMARC readiness are
        separate. DNS propagation usually takes minutes and occasionally hours, so poll at a sane
        interval or subscribe to the `domain.verified` webhook instead. Domains are also
        rechecked in the background: a verified domain whose DKIM record stops resolving gets
        `dkim_missing_since`, keeps sending, and `domain.at_risk` is sent; `domain.restored`
        follows if the record is back, and has held for an hour, by `stops_sending_at`, otherwise
        it loses `verified_at` and `domain.lost` is sent.
        """
        return await self._request(
            "POST",
            f"/domains/{path_segment(domain_id)}/verify",
            timeout=timeout,
        )

    async def diagnostics(
        self,
        domain_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[DnsDiagnosticsResponse]:
        """Diagnose domain DNS configuration.

        Reads the domain's live DNS zone and reports what is wrong with it — a duplicate SPF
        record, a permissive policy, a missing return path. Each finding carries a severity, an
        explanation, the fix, and the records it was drawn from. Nothing is stored; the result
        always reflects DNS as it is right now.
        """
        return await self._request(
            "GET",
            f"/domains/{path_segment(domain_id)}/diagnostics",
            timeout=timeout,
        )


class AsyncRawMailboxes(AsyncRawResource):
    """Connect and manage provider mailboxes."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[MailboxPage]:
        """List mailboxes.

        Lists connected Gmail and Outlook mailboxes with their sync state.
        """
        return await self._request(
            "GET",
            "/mailboxes",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    async def connect(
        self,
        params: ConnectMailboxRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[ConnectMailboxResponse]:
        """Create a mailbox connection URL.

        Creates a single-use, short-lived URL that walks a customer through authorizing their
        Gmail or Outlook mailbox. Redirect them to it rather than emailing it. Pass `ref` — your
        own identifier — and `metadata` for anything else you want kept with the mailbox; both
        are stored on it and carried on every `mailbox.*` webhook. On a reconnect each replaces
        what the mailbox had, and one left out leaves it alone. The `mailbox.connected` webhook —
        not the browser returning to `return_to` — is the authoritative signal that the mailbox
        is live. `return_to` may be any URL here, since the request is authenticated; a connect
        link opened from a browser is held to the app's `return_urls` instead. `space_id` files
        the mailbox in a space; the returned URL carries it, so a platform mints one link per
        customer server-side rather than handing out the bare hosted link. A workspace with no
        plan fails with 402 `plan_required`. A mailbox counts against the plan's mailboxes, but
        which one it will be is only known once the person has authorized: with none left, a
        mailbox the workspace does not already hold is refused then, and the refusal is reported
        in `error` on `return_to`. Reconnecting one that is `active` or `needs_reauth` takes
        nothing new.
        """
        return await self._request(
            "POST",
            "/mailboxes/connect",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Mailbox]:
        """Retrieve a mailbox.

        Returns one mailbox, including its `state` and the provider's `state_reason` when there
        is one. A mailbox that is not `active` cannot send.
        """
        return await self._request(
            "GET",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    async def disconnect(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Mailbox]:
        """Disconnect a mailbox.

        Disconnects a mailbox, stopping sync and dropping its stored credentials. Messages
        already received stay on their threads.
        """
        return await self._request(
            "DELETE",
            f"/mailboxes/{path_segment(mailbox_id)}",
            timeout=timeout,
        )

    async def sync(
        self,
        mailbox_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[MailboxSyncResponse]:
        """Queue a mailbox sync.

        Queues a catch-up sync for a mailbox. Mail normally arrives on its own through provider
        push notifications, so this is a repair tool rather than a way to poll. Messages found
        surface as ordinary `email.received` events.
        """
        return await self._request(
            "POST",
            f"/mailboxes/{path_segment(mailbox_id)}/sync",
            timeout=timeout,
        )


class AsyncRawOauthApps(AsyncRawResource):
    """Manage customer-owned Google and Microsoft OAuth apps."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthAppPage]:
        """List OAuth apps.

        Lists the workspace's own Google and Microsoft OAuth apps.
        """
        return await self._request(
            "GET",
            "/oauth-apps",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    async def create(
        self,
        params: CreateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthApp]:
        """Create an OAuth app.

        Registers your own OAuth app so the mailbox consent screen carries your product's name
        rather than AI Inbx. The response returns the `redirect_uri` to register with the
        provider, a hosted `connect_url`, and — for Google — the `push_endpoint` your own Pub/Sub
        topic should publish to. The `slug` is claimed globally because it forms the connect URL.
        `return_urls` lists the pages of yours a connect link (`connect_url` +
        `/start?return_to=…`) may send a person back to; without one, only the hosted page works.
        """
        return await self._request(
            "POST",
            "/oauth-apps",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthApp]:
        """Retrieve an OAuth app.

        Returns one OAuth app. The client secret is never returned.
        """
        return await self._request(
            "GET",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        app_id: str,
        params: UpdateOAuthAppRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[OAuthApp]:
        """Update an OAuth app.

        Updates an OAuth app's credentials, branding or return URLs. At least one field is
        required. A rotated secret replaces the old one immediately, so update the provider
        first. `return_urls` replaces the whole list.
        """
        return await self._request(
            "PATCH",
            f"/oauth-apps/{path_segment(app_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        app_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete an OAuth app.

        Deletes an OAuth app. Mailboxes already connected through it keep working until their
        authorization lapses.
        """
        return await self._request(
            "DELETE",
            f"/oauth-apps/{path_segment(app_id)}",
            timeout=timeout,
        )


class AsyncRawWebhookEndpoints(AsyncRawResource):
    """Configure event delivery and inspect delivery attempts."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpointPage]:
        """List webhook endpoints.

        Lists the workspace's webhook endpoints with their subscriptions and routing rules.
        """
        return await self._request(
            "GET",
            "/webhook-endpoints",
            params={
                "limit": limit,
                "cursor": cursor,
            },
            timeout=timeout,
        )

    async def create(
        self,
        params: WebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpointCreated]:
        """Create a webhook endpoint.

        Registers an organization-wide endpoint and returns its signing secret exactly once, in
        the `secret` field: no later read shows it again. A secret that was lost, or has leaked,
        is replaced with `POST /webhook-endpoints/{endpoint_id}/rotate-secret`, which keeps the
        old one verifying for a grace period while you deploy the new one. `subscriptions` must
        name at least one event type. Setting `payload` to `full` puts the whole email on
        `email.received` and `email.sent`, as `data.email`, so a handler does not have to fetch
        it. Optional routing rules narrow delivery by sender or recipient: a matching `block`
        rule always wins, and an empty allow list means no opinion. The endpoint receives every
        space's events, each stamped with its `space_id`.
        """
        return await self._request(
            "POST",
            "/webhook-endpoints",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpoint]:
        """Retrieve a webhook endpoint.

        Returns one endpoint, including when a rotated previous secret stops being accepted.
        """
        return await self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        endpoint_id: str,
        params: UpdateWebhookEndpointRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEndpoint]:
        """Update a webhook endpoint.

        Updates an endpoint's URL, subscriptions, routing rules, payload, or enabled state. At
        least one field is required. A change of `payload` applies from the next delivery
        attempt, retries of earlier events included; a `v1` endpoint cannot be `full`. A disabled
        endpoint receives nothing, and events that occur while it is off are not queued for
        later.
        """
        return await self._request(
            "PATCH",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        endpoint_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a webhook endpoint.

        Deletes an endpoint. Pending deliveries to it stop.
        """
        return await self._request(
            "DELETE",
            f"/webhook-endpoints/{path_segment(endpoint_id)}",
            timeout=timeout,
        )

    async def rotate_secret(
        self,
        endpoint_id: str,
        params: RotateWebhookSecretRequest | None = None,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookSecretResponse]:
        """Rotate a webhook signing secret.

        Issues a new signing secret and returns it, once — the only way to get a secret after the
        endpoint was created. The previous one keeps verifying for `grace_seconds` (a day by
        default, a week at most): every delivery in that window is signed with both, so a
        deployment can roll over without dropping events, and `previous_secret_expires_at` says
        when the overlap ends. Set the grace period to 0 only when a secret has leaked and the
        exposure matters more than the gap.
        """
        return await self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/rotate-secret",
            json=params or {},
            timeout=timeout,
        )

    async def test(
        self,
        endpoint_id: str,
        params: WebhookTestRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookTestResponse]:
        """Send a test webhook.

        Delivers a synthetic event to the endpoint and reports what it actually did — status
        code, duration, error, and the first 2 KB of its response. The test event is signed like
        a real one, so it exercises signature verification too. `payload` is sent verbatim and
        does not have to match the real shape for that event type. A test event is about no
        message, so on a `full` endpoint the `data.email` of an `email.received` or `email.sent`
        test is the `email` you put in `payload`, or null.
        """
        return await self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/test",
            json=params,
            timeout=timeout,
        )

    async def list_deliveries(
        self,
        endpoint_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        state: Literal["pending", "delivered", "failed"] | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookDeliveryPage]:
        """List webhook deliveries.

        Lists deliveries to an endpoint, filterable by state. Each carries the event envelope it
        sends and every attempt made: timestamp, status code, duration, error, and the beginning
        of your response, which is usually what explains a rejection. `body` is what is stored.
        For a `full` endpoint that is the envelope without `data.email`: the email is read from
        the message each time a delivery is sent and is not kept with it. It is null for a `v1`
        endpoint — its legacy body is built from the message at send time, not stored — and for a
        delivery nothing was sent for.
        """
        return await self._request(
            "GET",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries",
            params={
                "limit": limit,
                "cursor": cursor,
                "state": state,
            },
            timeout=timeout,
        )

    async def retry_deliveries(
        self,
        endpoint_id: str,
        params: RetryDeliveriesRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[IdListResponse]:
        """Retry webhook deliveries.

        Replays up to 100 deliveries. A replay carries the same event `id` as the original, so a
        handler that deduplicates on it stays correct.
        """
        return await self._request(
            "POST",
            f"/webhook-endpoints/{path_segment(endpoint_id)}/deliveries/retry",
            json=params,
            timeout=timeout,
        )


class AsyncRawEvents(AsyncRawResource):
    """Read back what happened in the workspace — the events webhooks carry, whether or not an
    endpoint heard them.
    """

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        after: str | None = None,
        before: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        type: Sequence[Literal["email.received", "email.sent", "email.delivered", "email.bounced", "email.complained", "email.failed", "email.unsubscribed", "email.opened", "email.clicked", "thread.created", "domain.verified", "domain.at_risk", "domain.restored", "domain.lost", "mailbox.connected", "mailbox.needs_reauth", "mailbox.disconnected"]] | None = None,
        email_id: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[EventPage]:
        """List events.

        Lists the workspace's events, newest first — every event, recorded when it happens,
        whether or not a webhook endpoint subscribes to its type. Each is the envelope a webhook
        delivers, with the same `id`, so a handler that deduplicates on it can read from here and
        from its endpoint alike. Filter by `type`, repeated for any of several, or by `email_id`
        for what happened to one email. To catch up after missed webhooks, walk forward:
        `order=asc` with `after` set to the `created_at` of the last event you processed. `data`
        is the summary every endpoint receives; the `data.email` a `full` endpoint is sent is
        read when a delivery goes out and not kept, so read the email by its `email_id`. Test
        events sent to an endpoint are not listed.
        """
        return await self._request(
            "GET",
            "/events",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "after": after,
                "before": before,
                "order": order,
                "type": type,
                "email_id": email_id,
            },
            timeout=timeout,
        )

    async def retrieve(
        self,
        event_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WebhookEvent]:
        """Retrieve an event.

        Returns one event by id — the `id` of the envelope a webhook delivered, which is also the
        `AIInbx-Event-ID` header and a delivery's `event_id`.
        """
        return await self._request(
            "GET",
            f"/events/{path_segment(event_id)}",
            timeout=timeout,
        )


class AsyncRawSuppressions(AsyncRawResource):
    """Prevent delivery to opted-out or unsafe recipients."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        key: str | None = None,
        address: str | None = None,
        reason: Literal["complaint", "bounce", "unsubscribe", "manual"] | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[SuppressionPage]:
        """List suppressions.

        Lists suppression entries, filterable by list `key`, `reason`, or a substring of the
        `address`. `blocks` and `last_blocked_at` show how often each entry has actually stopped
        a send.
        """
        return await self._request(
            "GET",
            "/suppressions",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
                "key": key,
                "address": address,
                "reason": reason,
            },
            timeout=timeout,
        )

    async def add(
        self,
        params: SuppressionRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[SuppressionBatch]:
        """Create suppressions.

        Adds up to 1000 addresses to a suppression list. `key` defaults to the workspace-wide `*`
        list and `scope` to `all`; a `scope` of `optional` blocks only sends marked as
        unsubscribable, so a marketing opt-out does not stop a password reset. Adding an address
        that is already listed updates the existing entry rather than duplicating it, and never
        narrows a wider scope. `space_id` puts the entries on a space's list, which stops that
        space's sends alone; without it they stop every space's.
        """
        return await self._request(
            "POST",
            "/suppressions",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Suppression]:
        """Retrieve a suppression.

        Returns one suppression entry, including how it was created and how many sends it has
        stopped.
        """
        return await self._request(
            "GET",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )

    async def remove(
        self,
        suppression_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[SuppressionDeleted]:
        """Delete a suppression.

        Removes a suppression entry, allowing sends to that address again. Removing a `bounce` or
        `complaint` entry means mailing an address that already rejected you or reported you as
        spam — do it only with specific evidence the address was fixed. `provider_suppressed`
        says whether SES itself still refuses the address, which removing the entry does not
        change.
        """
        return await self._request(
            "DELETE",
            f"/suppressions/{path_segment(suppression_id)}",
            timeout=timeout,
        )


class AsyncRawPacingRules(AsyncRawResource):
    """Rules that pace outgoing mail: sending hours, and caps per sender, recipient or domain."""

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRulePage]:
        """List pacing rules.

        Lists the workspace's pacing rules, both sending-hours and rate-limit kinds. Rules with
        `builtin: true` came with the workspace: they cap mail sent from the [provided
        domain](/guides/domains#your-provided-domain) and cannot be changed or removed.
        """
        return await self._request(
            "GET",
            "/pacing-rules",
            params={
                "limit": limit,
                "cursor": cursor,
                "space": space,
            },
            timeout=timeout,
        )

    async def create(
        self,
        params: PacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRule]:
        """Create a pacing rule.

        Creates a pacing rule. An `hours` rule holds mail outside the weekly windows you declare,
        evaluated in the rule's own timezone. A `limit` rule caps sends per rolling window
        against a scope — the rule as a whole, or per sender address, sending domain, recipient,
        or recipient domain. An empty `match` array applies the rule to every send. `space_id`
        makes the rule read one space's mail alone; workspace rules apply to every space and
        stack on top. An enabled rule counts against the plan's active custom pacing rules: with
        none left the request fails with 402 `allowance_reached`, and a workspace with no plan
        with 402 `plan_required`. A rule created with `enabled` false takes nothing until it is
        switched on.
        """
        return await self._request(
            "POST",
            "/pacing-rules",
            json=params,
            timeout=timeout,
        )

    async def retrieve(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRule]:
        """Retrieve a pacing rule.

        Returns one pacing rule with its match patterns and its schedule or limit.
        """
        return await self._request(
            "GET",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    async def update(
        self,
        rule_id: str,
        params: UpdatePacingRuleRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingRule]:
        """Update a pacing rule.

        Updates a pacing rule. At least one field is required. Setting `enabled` to false parks a
        rule without losing its configuration, which is the quickest way to confirm which rule is
        holding mail. A `builtin` rule cannot be changed and fails with `rule_builtin`. Setting
        `enabled` to true on a parked rule takes one of the plan's active custom pacing rules
        again, and fails with 402 `allowance_reached` when none is left.
        """
        return await self._request(
            "PATCH",
            f"/pacing-rules/{path_segment(rule_id)}",
            json=params,
            timeout=timeout,
        )

    async def delete(
        self,
        rule_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Delete a pacing rule.

        Deletes a pacing rule. Messages it was holding become eligible to send as soon as the
        remaining rules allow. A `builtin` rule cannot be deleted and fails with `rule_builtin`.
        """
        return await self._request(
            "DELETE",
            f"/pacing-rules/{path_segment(rule_id)}",
            timeout=timeout,
        )

    async def retrieve_spread(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingSpread]:
        """Retrieve pacing spread.

        Returns the workspace's send-timing spread, a value from 0 to 100.
        """
        return await self._request(
            "GET",
            "/pacing-rules/spread",
            timeout=timeout,
        )

    async def update_spread(
        self,
        params: PacingSpreadRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[PacingSpread]:
        """Update pacing spread.

        Sets how much randomness is added to send timing. At 0 a rate-limited stream goes out on
        a metronome; higher values vary the gaps, costing a little throughput in exchange for
        traffic that does not look machine-generated. Applies to limit rules.
        """
        return await self._request(
            "PATCH",
            "/pacing-rules/spread",
            json=params,
            timeout=timeout,
        )


class AsyncRawPacing(AsyncRawResource):
    """The mail pacing holds right now, the rule holding each, and releasing it early."""

    async def retrieve(
        self,
        *,
        limit: int | None = None,
        space: str | None = None,
        timeout: Timeout = None,
    ) -> RawResponse[PacingQueue]:
        """Retrieve the pacing queue.

        Returns a snapshot of everything pacing is currently holding: a sample of queued
        messages, the rules in effect, and per-rule counts of how many messages each matched and
        how many it is holding. The per-rule counts are the fastest way to identify which rule is
        responsible.
        """
        return await self._request(
            "GET",
            "/pacing-queue",
            params={
                "limit": limit,
                "space": space,
            },
            timeout=timeout,
        )

    async def release(
        self,
        params: PacingReleaseRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[IdListResponse]:
        """Release emails from the pacing queue.

        Releases up to 500 held emails immediately. `count_toward_limits` defaults to true;
        setting it to false means the sends do not consume rule budget, which makes the rule
        under-count — reserve it for genuinely exceptional releases. For mail that should never
        queue, set `pacing.skip` on the send instead.
        """
        return await self._request(
            "POST",
            "/pacing-queue/release",
            json=params,
            timeout=timeout,
        )


class AsyncRawWorkspaces(AsyncRawResource):
    """The workspace a request acts in: its name, and the defaults new domains start with."""

    async def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[WorkspaceList]:
        """List workspaces.

        Lists the workspaces the caller can act in, with its role in each. An API key reaches its
        own workspace alone. An OAuth token reaches every workspace it was granted, and a request
        with one that reaches several names the workspace it acts in with the `AIInbx-Workspace`
        header, set to an `id` from here; this list is the one call that needs no header. `mode`
        says whether the caller acts as the whole of its workspaces or as an inbox; a token
        connected as an inbox reaches the workspaces of its inboxes, and `inboxes` names the
        addresses it reads and sends as.
        """
        return await self._request(
            "GET",
            "/workspaces",
            timeout=timeout,
        )

    async def retrieve(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Workspace]:
        """Retrieve the workspace.

        Returns the workspace the request acts in: its name, its slug, and the tracking defaults
        a domain added from now on starts with.
        """
        return await self._request(
            "GET",
            "/workspace",
            timeout=timeout,
        )

    async def update(
        self,
        params: UpdateWorkspaceRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Workspace]:
        """Update the workspace.

        Renames the workspace or changes its tracking defaults; only the fields given change. A
        new name brings a new slug, which moves the console URLs with it (the provided domain
        keeps its name), so a workspace can be renamed once a month — sooner fails with 409
        `rename_cooldown`. Tracking defaults apply to domains added from now on; each existing
        domain keeps its own. Admin only.
        """
        return await self._request(
            "PATCH",
            "/workspace",
            json=params,
            timeout=timeout,
        )


class AsyncRawMembers(AsyncRawResource):
    """Who is in the workspace and what each of them may do. Admin only."""

    async def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[MemberList]:
        """List members.

        Lists everyone in the workspace, earliest to join first, with their role and when they
        were last active. A workspace holds at most 100 members, so the list is never paged.
        Admin only.
        """
        return await self._request(
            "GET",
            "/members",
            timeout=timeout,
        )

    async def update(
        self,
        member_id: str,
        params: UpdateMemberRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Member]:
        """Update a member.

        Changes what a member may do: `admin` manages the workspace, its members and its keys;
        `member` works with mail. It takes effect on their next request. The owner's role is not
        changed here — 409 `owner_protected` — the workspace changes hands by a transfer, in the
        console. Admin only.
        """
        return await self._request(
            "PATCH",
            f"/members/{path_segment(member_id)}",
            json=params,
            timeout=timeout,
        )

    async def remove(
        self,
        member_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Remove a member.

        Takes a member's access away at once. The mail they sent and the API keys they created
        stay with the workspace. The owner cannot be removed (409 `owner_protected`). Admin only.
        """
        return await self._request(
            "DELETE",
            f"/members/{path_segment(member_id)}",
            timeout=timeout,
        )


class AsyncRawInvitations(AsyncRawResource):
    """Invitations to join the workspace, waiting to be accepted. Admin only."""

    async def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[InvitationList]:
        """List invitations.

        Lists the invitations nobody has answered, newest first — lapsed ones too, past their
        `expires_at`: those can no longer be accepted, and inviting the address again sends a
        fresh one. Admin only.
        """
        return await self._request(
            "GET",
            "/invitations",
            timeout=timeout,
        )

    async def create(
        self,
        params: CreateInvitationRequest,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[Invitation]:
        """Invite someone.

        Mails an invitation to join the workspace, with a link that is good for seven days.
        Inviting an address that already has one waiting replaces it once the new mail has gone —
        the earlier link then stops working — which is also how an invitation is sent again. An
        address that is already a member fails with 409 `already_member`. When the mail cannot
        go, nothing is created and any earlier invitation keeps working: the address has been
        invited too often today, or the inviter has sent too many, fails with 429
        `invitation_not_sent` — try again later; an address that asked not to hear from us fails
        with 400 `recipients_suppressed`, which will not change on retrying. Invitations sent
        with an API key are in the name of the person who created the key, or the owner once they
        are gone. Admin only.
        """
        return await self._request(
            "POST",
            "/invitations",
            json=params,
            timeout=timeout,
        )

    async def cancel(
        self,
        invitation_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Cancel an invitation.

        Cancels an invitation that is waiting to be accepted; the link in the mail stops working.
        Send a new one if they still need it. Admin only.
        """
        return await self._request(
            "DELETE",
            f"/invitations/{path_segment(invitation_id)}",
            timeout=timeout,
        )


class AsyncRawAttachments(AsyncRawResource):
    """Download original and prepared attachment content."""

    async def download(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[bytes]:
        """Download an attachment.

        Redirects to a short-lived signed URL for the attachment's original bytes. Follow the
        redirect; the signed URL expires, so resolve it on demand rather than storing it.
        """
        return await self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
            binary=True,
        )

    async def inspect(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[None]:
        """Inspect attachment metadata.

        Returns the attachment's media type, size, and filename disposition in response headers
        without transferring the file — the cheap way to check a size before committing to a
        download.
        """
        return await self._request(
            "HEAD",
            f"/attachments/{path_segment(attachment_id)}",
            timeout=timeout,
        )

    async def content(
        self,
        attachment_id: str,
        *,
        timeout: Timeout = None,
    ) -> RawResponse[str]:
        """Download prepared attachment text.

        Redirects to a short-lived signed URL for the attachment's prepared text — Markdown where
        the document has structure, plain text otherwise. Returns 404 `not_prepared` when the
        file type has no text to extract or preparation failed.
        """
        return await self._request(
            "GET",
            f"/attachments/{path_segment(attachment_id)}/content",
            timeout=timeout,
            binary=True,
        )
