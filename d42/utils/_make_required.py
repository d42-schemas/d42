from typing import Any, List, Optional, Set, Tuple, Union

from niltype import Nil

from d42.declaration.errors import DeclarationError
from d42.declaration.types import DictSchema

__all__ = ("make_required",)


RequiredKeysType = Union[Set[str], List[str], Tuple[str, ...]]


def make_required(schema: Union[DictSchema, Any],
                  keys: Optional[RequiredKeysType] = None) -> DictSchema:
    if not isinstance(schema, DictSchema):
        message = f"Inappropriate type of schema {schema!r} ({type(schema)!r})"
        raise DeclarationError(message)

    if not isinstance(keys, (set, list, tuple, type(None))):
        message = f"Inappropriate type of keys {keys!r} ({type(keys)!r})"
        raise DeclarationError(message)

    if keys is None:
        keys = set(schema.keys())

    props_keys = schema.props.keys if (schema.props.keys is not Nil) else {}
    for key in keys:
        if key not in props_keys:
            message = f"Nonexisting key {key!r}"
            raise DeclarationError(message)

    if schema.props.keys is Nil:
        return schema
    else:
        updated_keys = {}
        for key, (val, is_optional) in props_keys.items():
            updated_keys[key] = (val, False if (key in keys) else is_optional)
        return schema.__class__(schema.props.update(keys=updated_keys))
