from typing import Any

from .._is_ellipsis import is_ellipsis

__all__ = ("optional", "is_absent", "is_present")


class _Absent:
    """Marker to indicate that an optional key must be absent in the data."""

    def __repr__(self) -> str:
        return "optional.absent"


class _Present:
    """Marker to indicate that a key must be present in the data (required field)."""

    def __repr__(self) -> str:
        return "optional.present"


def is_absent(value: Any) -> bool:
    return isinstance(value, _Absent)


def is_present(value: Any) -> bool:
    return isinstance(value, _Present)


class optional:
    absent = _Absent()
    present = _Present()

    def __init__(self, key: Any) -> None:
        if is_ellipsis(key):
            raise TypeError(key)
        self._key = key

    @property
    def key(self) -> Any:
        return self._key

    def __repr__(self) -> str:
        return f"optional({self._key!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and (self._key == other.key)

    def __hash__(self) -> int:
        return hash((self._key,))
