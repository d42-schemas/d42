import sys
from typing import Any

from niltype import Nil, Nilable

from .._is_ellipsis import TypeOrEllipsis, is_ellipsis
from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import (
    make_already_declared_error,
    make_incorrect_len_error,
    make_incorrect_max_len_error,
    make_incorrect_min_len_error,
    make_invalid_type_error,
)
from ._schema import Schema

__all__ = ("BytesSchema", "BytesProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class BytesProps(Props):
    @property
    def value(self) -> Nilable[bytes]:
        return self.get("value")

    @property
    def len(self) -> Nilable[int]:
        return self.get("len")

    @property
    def min_len(self) -> Nilable[int]:
        return self.get("min_len")

    @property
    def max_len(self) -> Nilable[int]:
        return self.get("max_len")


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

        if self.props.len is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min_len is not Nil) or (self.props.max_len is not Nil):
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))

    def __declare_len(self, props: BytesProps, length: Any) -> BytesProps:
        if not isinstance(length, int):
            raise make_invalid_type_error(self, length, (int,))

        if (props.value is not Nil) and (len(props.value) != length):
            raise make_incorrect_len_error(self, props.value, length)

        return props.update(len=length)

    def __declare_min_len(self, props: BytesProps, min_length: Any) -> BytesProps:
        if not isinstance(min_length, int):
            raise make_invalid_type_error(self, min_length, (int,))

        if (props.value is not Nil) and (min_length > len(props.value)):
            raise make_incorrect_min_len_error(self, props.value, min_length)

        return props.update(min_len=min_length)

    def __declare_max_len(self, props: BytesProps, max_length: Any) -> BytesProps:
        if not isinstance(max_length, int):
            raise make_invalid_type_error(self, max_length, (int,))

        if (props.value is not Nil) and (max_length < len(props.value)):
            raise make_incorrect_max_len_error(self, props.value, max_length)

        return props.update(max_len=max_length)

    def len(
        self,
        /,
        val_or_min: TypeOrEllipsis[int],
        max: Nilable[TypeOrEllipsis[int]] = Nil,
    ) -> "BytesSchema":
        if self.props.len is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min_len is not Nil) or (self.props.max_len is not Nil):
            raise make_already_declared_error(self)

        props = self.props
        if is_ellipsis(val_or_min):
            props = self.__declare_max_len(props, max)
        else:
            if max is Nil:
                props = self.__declare_len(props, val_or_min)
            elif is_ellipsis(max):
                props = self.__declare_min_len(props, val_or_min)
            else:
                props = self.__declare_max_len(
                    self.__declare_min_len(props, val_or_min),
                    max,
                )

        return self.__class__(props)
