import time
from typing import Any, Dict, Tuple


class MemoryCache:
    def __init__(self):
        self._store: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str):
        if key not in self._store:
            return None

        expires_at, value = self._store[key]

        if time.time() > expires_at:
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl_seconds: int):
        expires_at = time.time() + ttl_seconds
        self._store[key] = (expires_at, value)


cache = MemoryCache()
