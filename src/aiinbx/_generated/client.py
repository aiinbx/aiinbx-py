# Generated from @workspace/api-contract by `bun run sdk:generate`. Do not edit.
from __future__ import annotations

from typing_extensions import TypedDict

from .._base import AsyncTransport, SyncTransport
from .._resources import (
    ApiKeys,
    AsyncApiKeys,
    AsyncAttachments,
    AsyncDomains,
    AsyncEmails,
    AsyncEvents,
    AsyncInvitations,
    AsyncMailboxes,
    AsyncMembers,
    AsyncOauthApps,
    AsyncPacing,
    AsyncPacingRules,
    AsyncRawApiKeys,
    AsyncRawAttachments,
    AsyncRawDomains,
    AsyncRawEmails,
    AsyncRawEvents,
    AsyncRawInvitations,
    AsyncRawMailboxes,
    AsyncRawMembers,
    AsyncRawOauthApps,
    AsyncRawPacing,
    AsyncRawPacingRules,
    AsyncRawSpaces,
    AsyncRawSuppressions,
    AsyncRawThreads,
    AsyncRawWebhookEndpoints,
    AsyncRawWorkspaces,
    AsyncSpaces,
    AsyncSuppressions,
    AsyncThreads,
    AsyncWebhookEndpoints,
    AsyncWorkspaces,
    Attachments,
    Domains,
    Emails,
    Events,
    Invitations,
    Mailboxes,
    Members,
    OauthApps,
    Pacing,
    PacingRules,
    RawApiKeys,
    RawAttachments,
    RawDomains,
    RawEmails,
    RawEvents,
    RawInvitations,
    RawMailboxes,
    RawMembers,
    RawOauthApps,
    RawPacing,
    RawPacingRules,
    RawSpaces,
    RawSuppressions,
    RawThreads,
    RawWebhookEndpoints,
    RawWorkspaces,
    Spaces,
    Suppressions,
    Threads,
    WebhookEndpoints,
    Workspaces,
)


class SharedHeaders(TypedDict, total=False):
    """What the client sends as a header on every request, by the argument that sets each."""

    workspace_id: str
    """Workspace id from `GET /workspaces`, for an OAuth token that reaches several. Sent as
    ``AIInbx-Workspace``.
    """


def shared_headers(values: SharedHeaders) -> dict[str, str]:
    """The headers ``values`` stand for."""
    headers: dict[str, str] = {}
    if "workspace_id" in values:
        headers["AIInbx-Workspace"] = values["workspace_id"]
    return headers


class Resources:
    """Every resource of the API, one namespace each."""

    def __init__(self, client: SyncTransport) -> None:
        self.spaces = Spaces(client)
        self.api_keys = ApiKeys(client)
        self.emails = Emails(client)
        self.threads = Threads(client)
        self.domains = Domains(client)
        self.mailboxes = Mailboxes(client)
        self.oauth_apps = OauthApps(client)
        self.webhook_endpoints = WebhookEndpoints(client)
        self.events = Events(client)
        self.suppressions = Suppressions(client)
        self.pacing_rules = PacingRules(client)
        self.pacing = Pacing(client)
        self.workspaces = Workspaces(client)
        self.members = Members(client)
        self.invitations = Invitations(client)
        self.attachments = Attachments(client)


class RawResources:
    """Every resource, answering with the raw response."""

    def __init__(self, client: SyncTransport) -> None:
        self.spaces = RawSpaces(client)
        self.api_keys = RawApiKeys(client)
        self.emails = RawEmails(client)
        self.threads = RawThreads(client)
        self.domains = RawDomains(client)
        self.mailboxes = RawMailboxes(client)
        self.oauth_apps = RawOauthApps(client)
        self.webhook_endpoints = RawWebhookEndpoints(client)
        self.events = RawEvents(client)
        self.suppressions = RawSuppressions(client)
        self.pacing_rules = RawPacingRules(client)
        self.pacing = RawPacing(client)
        self.workspaces = RawWorkspaces(client)
        self.members = RawMembers(client)
        self.invitations = RawInvitations(client)
        self.attachments = RawAttachments(client)


class AsyncResources:
    """Every resource of the API, one namespace each."""

    def __init__(self, client: AsyncTransport) -> None:
        self.spaces = AsyncSpaces(client)
        self.api_keys = AsyncApiKeys(client)
        self.emails = AsyncEmails(client)
        self.threads = AsyncThreads(client)
        self.domains = AsyncDomains(client)
        self.mailboxes = AsyncMailboxes(client)
        self.oauth_apps = AsyncOauthApps(client)
        self.webhook_endpoints = AsyncWebhookEndpoints(client)
        self.events = AsyncEvents(client)
        self.suppressions = AsyncSuppressions(client)
        self.pacing_rules = AsyncPacingRules(client)
        self.pacing = AsyncPacing(client)
        self.workspaces = AsyncWorkspaces(client)
        self.members = AsyncMembers(client)
        self.invitations = AsyncInvitations(client)
        self.attachments = AsyncAttachments(client)


class AsyncRawResources:
    """Every resource, answering with the raw response."""

    def __init__(self, client: AsyncTransport) -> None:
        self.spaces = AsyncRawSpaces(client)
        self.api_keys = AsyncRawApiKeys(client)
        self.emails = AsyncRawEmails(client)
        self.threads = AsyncRawThreads(client)
        self.domains = AsyncRawDomains(client)
        self.mailboxes = AsyncRawMailboxes(client)
        self.oauth_apps = AsyncRawOauthApps(client)
        self.webhook_endpoints = AsyncRawWebhookEndpoints(client)
        self.events = AsyncRawEvents(client)
        self.suppressions = AsyncRawSuppressions(client)
        self.pacing_rules = AsyncRawPacingRules(client)
        self.pacing = AsyncRawPacing(client)
        self.workspaces = AsyncRawWorkspaces(client)
        self.members = AsyncRawMembers(client)
        self.invitations = AsyncRawInvitations(client)
        self.attachments = AsyncRawAttachments(client)
