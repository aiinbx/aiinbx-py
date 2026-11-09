"""The resources as the client exposes them: everything the contract
generates, plus what only an SDK can offer — walking a thread's messages.
The contract's ``extended`` list says which classes are subclassed here.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from ._base import Timeout
from ._generated.resources import (
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
    AsyncWebhookEndpoints,
    AsyncWorkspaces,
    Attachments,
    Domains,
    Emails,
    Events,
    GeneratedAsyncThreads,
    GeneratedThreads,
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
    WebhookEndpoints,
    Workspaces,
)
from .models import FullEmail, FullThread

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
    "AsyncThreads",
    "AsyncWebhookEndpoints",
    "AsyncWorkspaces",
    "Attachments",
    "Domains",
    "Emails",
    "Events",
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
    "Threads",
    "WebhookEndpoints",
    "Workspaces",
]


def _next_message_cursor(thread: FullThread, seen: set[str]) -> str | None:
    cursor = thread["messages_next_cursor"]
    if not cursor:
        return None
    if cursor in seen:
        raise RuntimeError("API returned the same message cursor more than once")
    seen.add(cursor)
    return cursor


class Threads(GeneratedThreads):
    def iter_messages(
        self,
        thread_id: str,
        *,
        message_limit: int | None = None,
        timeout: Timeout = None,
    ) -> Iterator[FullEmail]:
        """Every message in a thread, oldest first, across every page."""
        cursor: str | None = None
        seen: set[str] = set()
        while True:
            thread = self.retrieve(
                thread_id,
                message_limit=message_limit,
                message_cursor=cursor,
                timeout=timeout,
            )
            yield from thread["messages"]
            cursor = _next_message_cursor(thread, seen)
            if cursor is None:
                return


class AsyncThreads(GeneratedAsyncThreads):
    async def iter_messages(
        self,
        thread_id: str,
        *,
        message_limit: int | None = None,
        timeout: Timeout = None,
    ) -> AsyncIterator[FullEmail]:
        """Every message in a thread, oldest first, across every page."""
        cursor: str | None = None
        seen: set[str] = set()
        while True:
            thread = await self.retrieve(
                thread_id,
                message_limit=message_limit,
                message_cursor=cursor,
                timeout=timeout,
            )
            for message in thread["messages"]:
                yield message
            cursor = _next_message_cursor(thread, seen)
            if cursor is None:
                return
