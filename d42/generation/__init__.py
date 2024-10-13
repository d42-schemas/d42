from typing import Any

from d42.declaration import GenericSchema, Schema

from ._generator import Generator
from ._random import Random
from ._regex_generator import RegexGenerator

__all__ = ("fake", "generate", "Generator", "Random", "RegexGenerator",)

_random = Random()
_generator = Generator(_random, RegexGenerator(_random))


def generate(schema: GenericSchema, **kwargs: Any) -> Any:
    if not isinstance(schema, Schema):
        raise TypeError("Expected 'schema' to be an instance of 'd42.declaration.types.Schema', "
                        f"got {schema} instead")
    return schema.__accept__(_generator, **kwargs)


fake = generate

Schema.__override__(Schema.__invert__.__name__, generate)
