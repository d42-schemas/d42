from typing import Any

from .._is_ellipsis import is_ellipsis

__all__ = ("optional",)


class optional:
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
