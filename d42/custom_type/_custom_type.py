import sys
from typing import Any, cast, final

if sys.version_info < (3, 11):
    Self = Any
else:
    from typing import Self

from niltype import Nil, Nilable
from th import PathHolder

from d42.declaration import PropsType, Schema
from d42.generation import Generator
from d42.representation import Representor
from d42.substitution import Substitutor
from d42.validation import ValidationResult, Validator

__all__ = ("CustomSchema",)


class CustomSchema(Schema[PropsType]):
    def __init__(self, props: Nilable[PropsType] = Nil) -> None:
        if type(self) is CustomSchema:
            raise TypeError(f"Cannot instantiate abstract class {self.__class__.__name__}")
        super().__init__(props)

    @final
    def __d42_represent__(self, visitor: Representor, *, indent: int = 0, **kwargs: Any) -> str:
        if represent_method := getattr(self, "__represent__", None):
            return cast(str, represent_method(visitor, indent=indent, **kwargs))
        return f"<{self.__class__.__name__}>"

    @final
    def __d42_generate__(self, visitor: Generator, **kwargs: Any) -> Any:
        if generate_method := getattr(self, "__generate__", None):
            return generate_method(visitor, **kwargs)
        raise NotImplementedError(
            f"{self.__class__.__name__} has no method '__generate__'")

    @final
    def __d42_validate__(self, visitor: Validator, *, value: Any = Nil,
                         path: Nilable[PathHolder] = Nil, **kwargs: Any) -> ValidationResult:
        if validate_method := getattr(self, "__validate__", None):
            res = validate_method(visitor, value=value, path=path or visitor.make_path(), **kwargs)
            return cast(ValidationResult, res)
        raise NotImplementedError(
            f"{self.__class__.__name__} has no method '__validate__'")

    @final
    def __d42_substitute__(self, visitor: Substitutor, *, value: Any = Nil, **kwargs: Any) -> Self:
        if substitute_method := getattr(self, "__substitute__", None):
            return cast(Self, substitute_method(visitor, value=value, **kwargs))
        raise NotImplementedError(
            f"{self.__class__.__name__} has no method '__substitute__'")
