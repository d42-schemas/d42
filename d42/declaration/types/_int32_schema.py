from typing import Any, cast

from niltype import Nil, Nilable

from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import (
    make_already_declared_error,
    make_incorrect_max_error,
    make_incorrect_min_error,
    make_invalid_type_error,
)
from ._int_schema import IntProps, IntSchema

__all__ = ("Int32Schema",)


class Int32Schema(IntSchema):
    _int32_min = -(2 ** 31)
    _int32_max = 2 ** 31 - 1

    def __init__(self, props: Nilable[IntProps] = Nil) -> None:
        super().__init__(props)
        if (self.props is not Nil) and (self.props.min is Nil):
            self._props = self.props.update(min=self._int32_min)
        if (self.props is not Nil) and (self.props.max is Nil):
            self._props = self.props.update(max=self._int32_max)

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        if hasattr(visitor, "visit_int32"):
            return cast(ReturnType, visitor.visit_int32(self, **kwargs))
        return visitor.visit_int(self, **kwargs)

    def __call__(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min is not Nil and self.props.min != self._int32_min) or \
           (self.props.max is not Nil and self.props.max != self._int32_max):
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))

    def min(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if (self.props.min is not Nil) and (self.props.min != self._int32_min):
            raise make_already_declared_error(self)

        if (self.props.value is not Nil) and (value > self.props.value):
            raise make_incorrect_min_error(self, self.props.value, value)

        # if (self.props.max is not Nil) and (value > self.props.max):
        #     raise make_incorrect_min_error(self, self.props.max, value)

        return self.__class__(self.props.update(min=value))

    def max(self, /, value: int) -> "IntSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if (self.props.max is not Nil) and (self.props.max != self._int32_max):
            raise make_already_declared_error(self)

        if (self.props.value is not Nil) and (value < self.props.value):
            raise make_incorrect_max_error(self, self.props.value, value)

        return self.__class__(self.props.update(max=value))
