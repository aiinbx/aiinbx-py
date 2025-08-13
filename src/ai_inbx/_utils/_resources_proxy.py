from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `ai_inbx.resources` module.

    This is used so that we can lazily import `ai_inbx.resources` only when
    needed *and* so that users can just import `ai_inbx` and reference `ai_inbx.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("ai_inbx.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
