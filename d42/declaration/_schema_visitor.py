from abc import ABC
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from .types import (
        AnySchema,
        BoolSchema,
        BytesSchema,
        DateSchema,
        DateTimeSchema,
        DictSchema,
        FloatSchema,
        GenericTypeAliasSchema,
        IntSchema,
        ListSchema,
        NoneSchema,
        StrSchema,
        TypeAliasPropsType,
        UUID4Schema,
    )

__all__ = ("SchemaVisitor", "SchemaVisitorReturnType",)

SchemaVisitorReturnType = TypeVar("SchemaVisitorReturnType")


class SchemaVisitor(ABC, Generic[SchemaVisitorReturnType]):
    def visit_none(self, schema: "NoneSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_bool(self, schema: "BoolSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_int(self, schema: "IntSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_float(self, schema: "FloatSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_str(self, schema: "StrSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_list(self, schema: "ListSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_dict(self, schema: "DictSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_any(self, schema: "AnySchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_bytes(self, schema: "BytesSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_type_alias(self, schema: "GenericTypeAliasSchema[TypeAliasPropsType]",
                         **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_uuid4(self, schema: "UUID4Schema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_datetime(self, schema: "DateTimeSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def visit_date(self, schema: "DateSchema", **kwargs: Any) -> SchemaVisitorReturnType:
        raise NotImplementedError()

    def __getattr__(self, name: Any) -> Any:
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}")

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if kwargs.get("extend", False) is not True:
            return
        parent = cls.__bases__[0]
        for name, value in cls.__dict__.items():
            if callable(value) and not name.startswith("__"):
                setattr(parent, name, value)
