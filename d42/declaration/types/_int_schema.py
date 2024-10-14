import sys
from typing import Any

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import (
    DeclarationError,
    make_already_declared_error,
    make_incorrect_max_error,
    make_incorrect_min_error,
    make_invalid_type_error,
)
from ._schema import Schema

__all__ = ("IntSchema", "IntProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class IntProps(Props):
    @property
    def value(self) -> Nilable[int]:
        return self.get("value")

    @property
    def min(self) -> Nilable[int]:
        return self.get("min")

    @property
    def max(self) -> Nilable[int]:
        return self.get("max")

    @property
    def multiple_of(self) -> Nilable[int]:
        return self.get("multiple_of")


class IntSchema(Schema[IntProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = int
    else:
        type: Any = int

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_int(self, **kwargs)

    def __call__(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min is not Nil) or (self.props.max is not Nil):
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))

    def min(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if self.props.min is not Nil:
            raise make_already_declared_error(self)

        if (self.props.value is not Nil) and (value > self.props.value):
            raise make_incorrect_min_error(self, self.props.value, value)

        return self.__class__(self.props.update(min=value))

    def max(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if self.props.max is not Nil:
            raise make_already_declared_error(self)

        if (self.props.value is not Nil) and (value < self.props.value):
            raise make_incorrect_max_error(self, self.props.value, value)

        return self.__class__(self.props.update(max=value))

    def multiple_of(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if value <= 0:
            raise DeclarationError(
                f"`{self!r}` multiple_of value must be greater than 0, {value} given")

        if self.props.multiple_of is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(multiple_of=value))
