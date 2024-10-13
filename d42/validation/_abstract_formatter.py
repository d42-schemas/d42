from abc import ABC, abstractmethod
from typing import Any

from .errors import (
    AlphabetValidationError,
    ExtraElementValidationError,
    ExtraKeyValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MaxValueValidationError,
    MinLengthValidationError,
    MinValueValidationError,
    MissingElementValidationError,
    MissingKeyValidationError,
    RegexValidationError,
    SchemaMismatchValidationError,
    SubstrValidationError,
    TypeValidationError,
    ValueValidationError,
)

__all__ = ("AbstractFormatter",)


class AbstractFormatter(ABC):
    @abstractmethod
    def format_type_error(self, error: TypeValidationError) -> str:
        pass

    @abstractmethod
    def format_value_error(self, error: ValueValidationError) -> str:
        pass

    @abstractmethod
    def format_min_value_error(self, error: MinValueValidationError) -> str:
        pass

    @abstractmethod
    def format_max_value_error(self, error: MaxValueValidationError) -> str:
        pass

    @abstractmethod
    def format_length_error(self, error: LengthValidationError) -> str:
        pass

    @abstractmethod
    def format_min_length_error(self, error: MinLengthValidationError) -> str:
        pass

    @abstractmethod
    def format_max_length_error(self, error: MaxLengthValidationError) -> str:
        pass

    @abstractmethod
    def format_alphabet_error(self, error: AlphabetValidationError) -> str:
        pass

    @abstractmethod
    def format_substr_error(self, error: SubstrValidationError) -> str:
        pass

    @abstractmethod
    def format_regex_error(self, error: RegexValidationError) -> str:
        pass

    @abstractmethod
    def format_missing_element_error(self, error: MissingElementValidationError) -> str:
        pass

    @abstractmethod
    def format_extra_element_error(self, error: ExtraElementValidationError) -> str:
        pass

    @abstractmethod
    def format_missing_key_error(self, error: MissingKeyValidationError) -> str:
        pass

    @abstractmethod
    def format_extra_key_error(self, error: ExtraKeyValidationError) -> str:
        pass

    @abstractmethod
    def format_schema_missmatch_error(self, error: SchemaMismatchValidationError) -> str:
        pass

    def __getattr__(self, name: Any) -> Any:
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}")

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if kwargs.get("extend", False) is not True:
            return
        parent = cls.__bases__[0]
        assert issubclass(parent, AbstractFormatter)
        for name, value in cls.__dict__.items():
            if callable(value) and not name.startswith("_"):
                setattr(parent, name, value)
