from typing import Any

from d42.declaration import GenericSchema, Schema

from ._substitutor import Substitutor
from ._validator import SubstitutorValidator

__all__ = ("substitute", "Substitutor", "SubstitutorValidator",)

_substitutor = Substitutor()


def substitute(schema: GenericSchema, value: Any, **kwargs: Any) -> Any:
    return schema.__accept__(_substitutor, value=value, **kwargs)


Schema.__override__(Schema.__mod__.__name__, substitute)
