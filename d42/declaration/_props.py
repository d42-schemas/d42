from typing import Any, Iterator, Mapping, TypeVar

from niltype import Nil, Nilable

__all__ = ("Props", "PropsType",)

PropsType = TypeVar("PropsType", bound="Props")


class Props:
    def __init__(self, registry: Nilable[Mapping[str, Any]] = Nil) -> None:
        self._registry = registry if (registry is not Nil) else {}

    def get(self, name: str, default: Nilable[Any] = Nil) -> Nilable[Any]:
        return self._registry.get(name, default)

    def set(self: PropsType, name: str, value: Any) -> PropsType:
        registry = {**self._registry, name: value}
        return self.__class__(registry)

    def update(self: PropsType, **keys: Any) -> PropsType:
        registry = {**self._registry, **keys}
        return self.__class__(registry)

    def __iter__(self) -> Iterator[str]:
        return iter(self._registry)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._registry}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        for key, val in self._registry.items():
            other_val = other.get(key)
            if val != other_val:
                return False

        for key, other_val in other._registry.items():
            val = self.get(key)
            if other_val != val:
                return False

        return True
