import re
import sys
from typing import Any

from niltype import Nil, Nilable

from .._is_ellipsis import TypeOrEllipsis, is_ellipsis
from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import (
    DeclarationError,
    make_already_declared_error,
    make_incorrect_len_error,
    make_incorrect_max_len_error,
    make_incorrect_min_len_error,
    make_invalid_type_error,
)
from ._schema import Schema

__all__ = ("StrSchema", "StrProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class StrProps(Props):
    @property
    def value(self) -> Nilable[str]:
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

    @property
    def alphabet(self) -> Nilable[str]:
        return self.get("alphabet")

    @property
    def substr(self) -> Nilable[str]:
        return self.get("substr")

    @property
    def pattern(self) -> Nilable[str]:
        return self.get("pattern")


class StrSchema(Schema[StrProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = str
    else:
        type: Any = str

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_str(self, **kwargs)

    def __call__(self, /, value: str) -> "StrSchema":
        if not isinstance(value, str):
            raise make_invalid_type_error(self, value, (str,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        if self.props.len is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min_len is not Nil) or (self.props.max_len is not Nil):
            raise make_already_declared_error(self)

        if self.props.alphabet is not Nil:
            raise make_already_declared_error(self)

        if self.props.substr is not Nil:
            raise make_already_declared_error(self)

        if self.props.pattern is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))

    def __declare_len(self, props: StrProps, length: Any) -> StrProps:
        if not isinstance(length, int):
            raise make_invalid_type_error(self, length, (int,))

        if (props.value is not Nil) and (len(props.value) != length):
            raise make_incorrect_len_error(self, props.value, length)

        return props.update(len=length)

    def __declare_min_len(self, props: StrProps, min_length: Any) -> StrProps:
        if not isinstance(min_length, int):
            raise make_invalid_type_error(self, min_length, (int,))

        if (props.value is not Nil) and (min_length > len(props.value)):
            raise make_incorrect_min_len_error(self, props.value, min_length)

        return props.update(min_len=min_length)

    def __declare_max_len(self, props: StrProps, max_length: Any) -> StrProps:
        if not isinstance(max_length, int):
            raise make_invalid_type_error(self, max_length, (int,))

        if (props.value is not Nil) and (max_length < len(props.value)):
            raise make_incorrect_max_len_error(self, props.value, max_length)

        return props.update(max_len=max_length)

    def len(self, /, val_or_min: TypeOrEllipsis[int],
            max: Nilable[TypeOrEllipsis[int]] = Nil) -> "StrSchema":
        if self.props.len is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min_len is not Nil) or (self.props.max_len is not Nil):
            raise make_already_declared_error(self)

        if self.props.pattern is not Nil:
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
                props = self.__declare_max_len(self.__declare_min_len(props, val_or_min), max)
        return self.__class__(props)

    def alphabet(self, /, letters: str) -> "StrSchema":
        if not isinstance(letters, str):
            raise make_invalid_type_error(self, letters, (str,))

        if self.props.alphabet is not Nil:
            raise make_already_declared_error(self)

        if self.props.pattern is not Nil:
            raise make_already_declared_error(self)

        if self.props.value is not Nil:
            missing_letters = {x for x in self.props.value if x not in letters}
            if len(missing_letters) > 0:
                message = f"`{self!r}` alphabet is missing letters: "
                message += repr("".join(sorted(missing_letters)))
                raise DeclarationError(message)

        return self.__class__(self.props.update(alphabet=letters))

    def contains(self, substr: str) -> "StrSchema":
        if not isinstance(substr, str):
            raise make_invalid_type_error(self, substr, (str,))

        if self.props.substr is not Nil:
            raise make_already_declared_error(self)

        if self.props.pattern is not Nil:
            raise make_already_declared_error(self)

        if self.props.value is not Nil:
            if substr not in self.props.value:
                message = f"`{self!r}` does not contain {substr!r}"
                raise DeclarationError(message)

        return self.__class__(self.props.update(substr=substr))

    def regex(self, pattern: str) -> "StrSchema":
        if not isinstance(pattern, str):
            raise make_invalid_type_error(self, pattern, (str,))

        if (self.props.pattern is not Nil) or (self.props.alphabet is not Nil) or \
           (self.props.len is not Nil) or (self.props.min_len is not Nil) or \
           (self.props.len is not Nil) or (self.props.substr is not Nil):
            raise make_already_declared_error(self)

        try:
            re.compile(pattern)
        except re.error as e:
            message = f"Invalid pattern ({e})"
            raise DeclarationError(message) from None

        if self.props.value is not Nil:
            if re.search(pattern, self.props.value) is None:
                message = f"`{self!r}` does not match {pattern!r}"
                raise DeclarationError(message)

        return self.__class__(self.props.update(pattern=pattern))
