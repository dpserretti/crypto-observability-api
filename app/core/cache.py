import asyncio
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta
from typing import Any


class InMemoryCache:
    def __init__(self, ttl_seconds: int):
        self._ttl = timedelta(seconds=ttl_seconds)
        self._data: dict[str, dict[str, Any]] = {}
        self._inflight: dict[str, asyncio.Task] = {}

    def get(self, key: str) -> dict | None:
        entry = self._data.get(key)
        if not entry:
            return None

        if datetime.utcnow() - entry["timestamp"] > self._ttl:
            del self._data[key]
            return None

        return entry

    def set(self, key: str, value: Any) -> None:
        self._data[key] = {
            "value": value,
            "timestamp": datetime.utcnow(),
        }

    async def get_or_set_async(
        self,
        key: str,
        fetcher: Callable[[], Awaitable[Any]],
    ) -> tuple[Any, bool]:
        cached = self.get(key)
        if cached:
            return cached["value"], True

        task = self._inflight.get(key)
        is_owner = task is None

        if is_owner:
            task = asyncio.create_task(fetcher())
            self._inflight[key] = task

        try:
            value = await task
        finally:
            if is_owner:
                self._inflight.pop(key, None)

        if is_owner:
            self.set(key, value)

        return value, False
