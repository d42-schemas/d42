from typing import Any

from d42.declaration.types import GenericSchema, Schema

from ._representor import Representor

__all__ = ("Representor", "represent",)


_representor = Representor()


def represent(self: GenericSchema, **kwargs: Any) -> str:
    return self.__accept__(_representor, **kwargs)


Schema.__override__("__repr__", represent)
