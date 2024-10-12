import sys
from typing import Any

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import Schema

__all__ = ("BytesSchema", "BytesProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class BytesProps(Props):
    @property
    def value(self) -> Nilable[bytes]:
        return self.get("value")


class BytesSchema(Schema[BytesProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = bytes
    else:
        type: Any = bytes

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_bytes(self, **kwargs)

    def __call__(self, /, value: bytes) -> "BytesSchema":
        if not isinstance(value, bytes):
            raise make_invalid_type_error(self, value, (bytes,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))
