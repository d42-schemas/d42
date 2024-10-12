from typing import Any
from uuid import UUID

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import Schema

__all__ = ("UUID4Schema", "UUID4Props",)


class UUID4Props(Props):
    @property
    def value(self) -> Nilable[UUID]:
        return self.get("value")


class UUID4Schema(Schema[UUID4Props]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_uuid4(self, **kwargs)

    def __call__(self, /, value: UUID) -> "UUID4Schema":
        if not isinstance(value, UUID):
            raise make_invalid_type_error(self, value, (UUID,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))
