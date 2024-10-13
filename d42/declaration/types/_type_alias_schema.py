from typing import Any, TypeVar, cast

from niltype import Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ._any_schema import AnySchema
from ._schema import GenericSchema, Schema

__all__ = ("TypeAliasSchema", "TypeAliasProps",
           "GenericTypeAliasSchema", "TypeAliasPropsType",)


class TypeAliasProps(Props):
    @property
    def type(self) -> GenericSchema:
        return cast(GenericSchema, self.get("type", AnySchema()))

    @property
    def name(self) -> Nilable[str]:
        return self.get("name")


TypeAliasPropsType = TypeVar("TypeAliasPropsType", bound=TypeAliasProps)


class GenericTypeAliasSchema(Schema[TypeAliasPropsType]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_type_alias(self, **kwargs)


class TypeAliasSchema(GenericTypeAliasSchema[TypeAliasProps]):
    pass
