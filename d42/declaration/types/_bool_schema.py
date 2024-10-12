import sys
from typing import Any

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import Schema

__all__ = ("BoolSchema", "BoolProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class BoolProps(Props):
    @property
    def value(self) -> Nilable[bool]:
        return self.get("value")


class BoolSchema(Schema[BoolProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = bool
    else:
        type: Any = bool

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_bool(self, **kwargs)

    def __call__(self, /, value: bool) -> "BoolSchema":
        if not isinstance(value, bool):
            raise make_invalid_type_error(self, value, (bool,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))
