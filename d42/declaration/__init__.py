from typing import Any, Type, TypeVar, cast

from ._props import Props, PropsType
from ._schema_facade import SchemaFacade
from ._schema_visitor import SchemaVisitor, SchemaVisitorReturnType
from .errors import DeclarationError
from .types import AnySchema, GenericSchema, Schema, optional

__all__ = ("schema", "GenericSchema", "Schema", "Props", "PropsType", "SchemaVisitor",
           "SchemaVisitorReturnType", "optional", "register_type", "union",
           "DeclarationError",)


schema = SchemaFacade()

_SchemaType = TypeVar("_SchemaType", bound=GenericSchema)


def register_type(name: str, schema_type: Type[_SchemaType]) -> _SchemaType:
    if not issubclass(schema_type, Schema):
        raise TypeError(f"{schema_type!r} must be a subclass of Schema")
    setattr(SchemaFacade, name, property(lambda self: schema_type()))
    return cast(_SchemaType, getattr(schema, name))


def union(self: GenericSchema, other: Any) -> AnySchema:
    return schema.any(self, other)


Schema.__override__("__or__", union)
