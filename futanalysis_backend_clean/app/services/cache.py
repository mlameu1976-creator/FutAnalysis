import time

_cache = {}


def get_cache(key: str):
    data = _cache.get(key)
    if not data:
        return None

    value, expires = data
    if time.time() > expires:
        del _cache[key]
        return None

    return value


def set_cache(key: str, value, ttl: int):
    _cache[key] = (value, time.time() + ttl)
