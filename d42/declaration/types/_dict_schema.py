import sys
from typing import Any, Dict, Generator, KeysView, Tuple

from niltype import Nil, Nilable

from .._is_ellipsis import TypeOrEllipsis, is_ellipsis
from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import DeclarationError, make_already_declared_error, make_invalid_type_error
from ._optional import optional
from ._schema import GenericSchema, Schema

__all__ = ("DictSchema", "DictProps", "optional",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class DictProps(Props):
    @property
    def keys(self) -> Nilable[Dict[Any, Tuple[GenericSchema, bool]]]:
        return self.get("keys")


class DictSchema(Schema[DictProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = Dict
    else:
        type: Any = Dict

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_dict(self, **kwargs)

    def __call__(self, /, keys: Dict[Any, TypeOrEllipsis[GenericSchema]]) -> "DictSchema":
        if not isinstance(keys, dict):
            raise make_invalid_type_error(self, keys, (dict,))

        if self.props.keys is not Nil:
            raise make_already_declared_error(self)

        real_keys = {}
        for key, val in keys.items():
            if is_ellipsis(key) or is_ellipsis(val):
                if not is_ellipsis(key):
                    message = f"Inappropriate type of key {key!r} ({type(key)!r})"
                    raise DeclarationError(message)
                if not is_ellipsis(val):
                    message = f"Inappropriate type of value {val!r} ({type(val)!r})"
                    raise DeclarationError(message)
            else:
                if not isinstance(val, Schema):
                    raise make_invalid_type_error(self, val, (Schema,))
            if isinstance(key, optional):
                real_keys[key.key] = (val, True)
            else:
                real_keys[key] = (val, False)

        return self.__class__(self.props.update(keys=real_keys))

    def __getitem__(self, /, key: Any) -> GenericSchema:
        if (self.props.keys is Nil) or (key not in self.props.keys) or (is_ellipsis(key)):
            key_repr = "..." if is_ellipsis(key) else key
            raise KeyError(key_repr)
        return self.props.keys[key][0]

    def __add__(self, /, other: "DictSchema") -> "DictSchema":
        if not isinstance(other, DictSchema):
            raise TypeError(
                f"Unsupported operand type for +: '{self.__class__.__name__}' and {type(other)!r}")

        self_keys = self.props.keys if (self.props.keys is not Nil) else {}
        other_keys = other.props.keys if (other.props.keys is not Nil) else {}
        merged_keys = {**self_keys, **other_keys}
        return self.__class__(self.props.update(keys=merged_keys))

    def keys(self) -> KeysView[Any]:
        if self.props.keys is Nil:
            return {}.keys()
        return self.props.keys.keys()

    def __iter__(self) -> Generator[Any, None, None]:
        yield from self.keys()
