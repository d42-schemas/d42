from abc import ABC
from typing import Any, Generic, cast

from niltype import Nil, Nilable

from .._props import PropsType
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType

__all__ = ("Schema", "GenericSchema",)


class Schema(ABC, Generic[PropsType]):
    type = Any

    def __init__(self, props: Nilable[PropsType] = Nil) -> None:
        if type(self) is Schema:
            raise TypeError(f"Cannot instantiate abstract class {self.__class__.__name__}")
        props_type = self.__orig_bases__[0].__args__[0]  # type: ignore
        self._props = cast(PropsType, props_type()) if props is Nil else props

    @property
    def props(self) -> PropsType:
        return self._props

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        if visit_method := getattr(visitor, "visit", None):
            return cast(ReturnType, visit_method(self, **kwargs))
        raise NotImplementedError(f"{visitor.__class__.__name__} has no method 'visit'")

    @classmethod
    def __override__(cls, method: str, fn: Any) -> None:
        setattr(cls, method, fn)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.props!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and (self.props == other.props)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __or__(self, other: Any) -> Any:
        raise AttributeError("Schema has no attribute '__or__'")

    def __invert__(self) -> Any:
        raise AttributeError("Schema has no attribute '__invert__'")

    def __mod__(self, other: Any) -> Any:
        raise AttributeError("Schema has no attribute '__mod__'")

    def __add__(self, other: Any) -> Any:
        raise AttributeError("Schema has no attribute '__add__'")


GenericSchema = Schema[Any]
