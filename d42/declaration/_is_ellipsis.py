from typing import TYPE_CHECKING, Any, TypeVar, Union

__all__ = ("is_ellipsis", "EllipsisType", "TypeOrEllipsis",)

if TYPE_CHECKING:
    import builtins
    EllipsisType = builtins.ellipsis
else:
    EllipsisType = Any


def is_ellipsis(value: Any) -> bool:
    return isinstance(value, type(...))


_T = TypeVar("_T")
TypeOrEllipsis = Union[_T, EllipsisType]
