from datetime import date
from typing import Any

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import Schema

__all__ = ("DateSchema", "DateProps",)


class DateProps(Props):
    @property
    def value(self) -> Nilable[date]:
        return self.get("value")


class DateSchema(Schema[DateProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_date(self, **kwargs)

    def __call__(self, /, value: date) -> "DateSchema":
        if not isinstance(value, date):
            raise make_invalid_type_error(self, value, (date,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))
