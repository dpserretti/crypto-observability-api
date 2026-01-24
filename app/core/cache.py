from datetime import datetime, timedelta
from typing import Any


class InMemoryCache:
    def __init__(self, ttl_seconds: int):
        self._ttl = timedelta(seconds=ttl_seconds)
        self._data: dict[str, dict[str, Any]] = {}

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
