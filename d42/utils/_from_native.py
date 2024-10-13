from datetime import date, datetime
from typing import Any
from uuid import UUID

from d42.declaration.types import (
    BoolSchema,
    BytesSchema,
    DateSchema,
    DateTimeSchema,
    DictSchema,
    FloatSchema,
    GenericSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    UUID4Schema,
)

__all__ = ("from_native",)


def from_native(value: Any) -> GenericSchema:
    if value is None:
        return NoneSchema()
    elif isinstance(value, bool):
        return BoolSchema()(value)
    elif isinstance(value, int):
        return IntSchema()(value)
    elif isinstance(value, float):
        return FloatSchema()(value)
    elif isinstance(value, str):
        return StrSchema()(value)
    elif isinstance(value, list):
        return ListSchema()([from_native(x) for x in value])
    elif isinstance(value, dict):
        return DictSchema()({key: from_native(val) for key, val in value.items()})
    elif isinstance(value, bytes):
        return BytesSchema()(value)
    elif isinstance(value, UUID) and (value.version == 4):
        return UUID4Schema()(value)
    elif isinstance(value, datetime):
        return DateTimeSchema()(value)
    elif isinstance(value, date):
        return DateSchema()(value)
    else:
        raise ValueError(value)
