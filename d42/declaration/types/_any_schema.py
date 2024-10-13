import sys
from typing import Any, Generator, Tuple

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import GenericSchema, Schema

__all__ = ("AnySchema", "AnyProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class AnyProps(Props):
    @property
    def types(self) -> Nilable[Tuple[GenericSchema, ...]]:
        return self.get("types")


class AnySchema(Schema[AnyProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = Any
    else:
        type: Any = Any

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_any(self, **kwargs)

    def __call__(self, /, type_: GenericSchema, *types: GenericSchema) -> "AnySchema":
        types_ = (type_,) + types
        for t in types_:
            if not isinstance(t, Schema):
                raise make_invalid_type_error(self, t, (Schema,))

        if self.props.types is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(types=types_))

    def __iter__(self) -> Generator[GenericSchema, None, None]:
        if self.props.types is not Nil:
            yield from self.props.types
        else:
            yield from ()
