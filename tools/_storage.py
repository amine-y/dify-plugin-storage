from typing import Any


def get_optional(storage: Any, key: str) -> bytes | None:
    """Return a stored value without treating a missing key as an error."""
    if not storage.exist(key):
        return None

    return storage.get(key)
