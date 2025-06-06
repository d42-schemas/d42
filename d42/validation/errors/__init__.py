import typing
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Type

from th import PathHolder

from d42.declaration import GenericSchema

if TYPE_CHECKING:
    from .._formatter import Formatter

__all__ = ("ValidationError", "TypeValidationError", "ValueValidationError",
           "MinValueValidationError", "MaxValueValidationError", "LengthValidationError",
           "MinLengthValidationError", "MaxLengthValidationError", "AlphabetValidationError",
           "SubstrValidationError", "RegexValidationError", "MissingElementValidationError",
           "ExtraElementValidationError", "MissingKeyValidationError", "ExtraKeyValidationError",
           "SchemaMismatchValidationError", "InvalidUUIDVersionValidationError",)


class ValidationError(ABC):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and (self.__dict__ == other.__dict__)

    @abstractmethod
    def format(self, formatter: "Formatter") -> str:
        pass


class TypeValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, expected_type: Type[Any]) -> None:
        self.path = path
        self.actual_value = actual_value
        self.expected_type = expected_type

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_type_error(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.path}, {self.actual_value!r}, "
            f"{self.expected_type})"
        )


class ValueValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, expected_value: Any) -> None:
        self.path = path
        self.actual_value = actual_value
        self.expected_value = expected_value

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_value_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.expected_value!r})")


class MinValueValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, min_value: Any) -> None:
        self.path = path
        self.actual_value = actual_value
        self.min_value = min_value

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_min_value_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.min_value!r})")


class MaxValueValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, max_value: Any) -> None:
        self.path = path
        self.actual_value = actual_value
        self.max_value = max_value

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_max_value_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.max_value!r})")


class LengthValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, length: int) -> None:
        self.path = path
        self.actual_value = actual_value
        self.length = length

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_length_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.length!r})")


class MinLengthValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, min_length: int) -> None:
        self.path = path
        self.actual_value = actual_value
        self.min_length = min_length

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_min_length_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.min_length!r})")


class MaxLengthValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, max_length: int) -> None:
        self.path = path
        self.actual_value = actual_value
        self.max_length = max_length

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_max_length_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.max_length!r})")


class AlphabetValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: str, alphabet: str) -> None:
        self.path = path
        self.actual_value = actual_value
        self.alphabet = alphabet

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_alphabet_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.alphabet!r})")


class SubstrValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, substr: str) -> None:
        self.path = path
        self.actual_value = actual_value
        self.substr = substr

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_substr_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.substr!r})")


class RegexValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, pattern: str) -> None:
        self.path = path
        self.actual_value = actual_value
        self.pattern = pattern

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_regex_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.pattern!r})")


class MissingElementValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, index: int) -> None:
        self.path = path
        self.actual_value = actual_value
        self.index = index

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_missing_element_error(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, {self.index!r})"


class ExtraElementValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, index: int) -> None:
        self.path = path
        self.actual_value = actual_value
        self.index = index

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_extra_element_error(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, {self.index!r})"


class MissingKeyValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, missing_key: Any) -> None:
        self.path = path
        self.actual_value = actual_value
        self.missing_key = missing_key

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_missing_key_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.missing_key!r})")


class ExtraKeyValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, extra_key: Any) -> None:
        self.path = path
        self.actual_value = actual_value
        self.extra_key = extra_key

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_extra_key_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.extra_key!r})")


class SchemaMismatchValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any,
                 expected_schemas: Tuple[GenericSchema, ...],
                 subschema_errors: Optional[
                     List[Tuple[int, List[ValidationError]]]] = None) -> None:
        self.path = path
        self.actual_value = actual_value
        self.expected_schemas = expected_schemas
        self.subschema_errors = subschema_errors
        self.schema_path: Optional[typing.List[int]] = None

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_schema_missmatch_error(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.path}, {self.actual_value!r}, "
            f"{self.expected_schemas}, {self.subschema_errors})"
        )


class InvalidUUIDVersionValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any,
                 actual_version: int, expected_version: int) -> None:
        self.path = path
        self.actual_value = actual_value
        self.actual_version = actual_version
        self.expected_version = expected_version

    def format(self, formatter: "Formatter") -> str:
        return formatter.format_invalid_uuid_version_error(self)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path!r}, {self.actual_value!r}, "
                f"{self.actual_version!r}, {self.expected_version!r})")
