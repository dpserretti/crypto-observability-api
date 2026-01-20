import time
from typing import Any


class InMemoryCache:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)

        if not entry:
            return None

        expires_at, value = entry

        if time.monotonic() > expires_at:
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        expires_at = time.monotonic() + self._ttl
        self._store[key] = (expires_at, value)
