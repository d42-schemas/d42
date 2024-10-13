from typing import Any, Dict, Union

from d42.declaration.types import optional
from d42.utils import is_ellipsis

__all__ = ("rollout",)


KeysType = Dict[Union[str, optional], Any]


def rollout(keys: KeysType, *, separator: str = ".") -> KeysType:
    updated: KeysType = {}

    for comp_key, val in keys.items():
        if is_ellipsis(comp_key):
            if not is_ellipsis(val):
                raise ValueError("Expected both key and value to be ellipsis")
            updated[comp_key] = val
            continue

        is_optional = False
        if isinstance(comp_key, optional):
            comp_key = comp_key.key
            is_optional = True
        if not isinstance(comp_key, str):
            raise TypeError(f"Unexpected key type {type(comp_key)}")

        parts = comp_key.split(separator)
        key = parts[0]
        if len(parts) == 1:
            updated[optional(key) if is_optional else key] = val
        else:
            if key not in updated:
                updated[key] = {}
            tail = separator.join(parts[1:])
            updated[key][optional(tail) if is_optional else tail] = val

    for k, v in updated.items():
        updated[k] = rollout(v, separator=separator) if isinstance(v, dict) else v

    return updated
