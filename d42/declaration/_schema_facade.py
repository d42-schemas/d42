from typing import Any

from .types import (
    AnySchema,
    BoolSchema,
    BytesSchema,
    DateSchema,
    DateTimeSchema,
    DictSchema,
    FloatSchema,
    GenericSchema,
    Int32Schema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    TypeAliasProps,
    TypeAliasSchema,
    UUID4Schema,
)

__all__ = ("SchemaFacade",)


class SchemaFacade:
    def alias(self, /, name: str, type_: GenericSchema) -> TypeAliasSchema:
        props = TypeAliasProps()
        return TypeAliasSchema(props.update(name=name, type=type_))

    @property
    def none(self) -> NoneSchema:
        return NoneSchema()

    @property
    def bool(self) -> BoolSchema:
        return BoolSchema()

    @property
    def int(self) -> IntSchema:
        return IntSchema()

    @property
    def int32(self) -> Int32Schema:
        return Int32Schema()

    @property
    def float(self) -> FloatSchema:
        return FloatSchema()

    @property
    def str(self) -> StrSchema:
        return StrSchema()

    @property
    def list(self) -> ListSchema:
        return ListSchema()

    @property
    def dict(self) -> DictSchema:
        return DictSchema()

    @property
    def any(self) -> AnySchema:
        return AnySchema()

    @property
    def bytes(self) -> BytesSchema:
        return BytesSchema()

    @property
    def uuid4(self) -> UUID4Schema:
        return UUID4Schema()

    @property
    def datetime(self) -> DateTimeSchema:
        return DateTimeSchema()

    @property
    def date(self) -> DateSchema:
        return DateSchema()

    def __getattr__(self, name: Any) -> Any:
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}")
