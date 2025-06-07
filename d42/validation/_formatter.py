import os
from copy import deepcopy
from typing import Any, List, Optional, Sequence

from th import PathHolder

from ._abstract_formatter import AbstractFormatter
from .errors import (
    AlphabetValidationError,
    ExtraElementValidationError,
    ExtraKeyValidationError,
    InvalidUUIDVersionValidationError,
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

__all__ = ("Formatter",)


class Formatter(AbstractFormatter):
    def __init__(self, root: str = "_") -> None:
        self._root = root

    @property
    def root(self) -> str:
        return self._root

    def _format_path(self, path: PathHolder) -> str:
        return str(path.__class__(self._root, [x for x in path]))

    def _at_path(self, path: PathHolder) -> str:
        return " at " + self._format_path(path) if len(path) > 0 else ""

    def _get_type(self, value: Any) -> str:
        return str(type(value))

    def _pluralize(self, count: int, options: Sequence[str]) -> str:
        return options[0] if count == 1 else options[-1]

    def format_type_error(self, error: TypeValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {error.actual_value!r}{formatted_path} "
                f"must be {error.expected_type}, but {actual_type} given")

    def format_value_error(self, error: ValueValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must be equal to {error.expected_value!r}, but {error.actual_value!r} given")

    def format_min_value_error(self, error: MinValueValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must be greater than or equal to {error.min_value!r}, "
                f"but {error.actual_value!r} given")

    def format_max_value_error(self, error: MaxValueValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must be less than or equal to {error.max_value!r}, "
                f"but {error.actual_value!r} given")

    def _format_length_error(self, path: PathHolder, actual_value: Any,
                             length: int, accuracy: str) -> str:
        actual_type = self._get_type(actual_value)
        actual_len = len(actual_value)
        formatted_path = self._at_path(path)
        options = ("element", "elements")
        return (
            f"Value {actual_type}{formatted_path} "
            f"must have {accuracy} {length} {self._pluralize(length, options)}, "
            f"but it has {actual_len} {self._pluralize(actual_len, options)}"
        )

    def format_length_error(self, error: LengthValidationError) -> str:
        return self._format_length_error(error.path, error.actual_value,
                                         error.length, "exactly")

    def format_min_length_error(self, error: MinLengthValidationError) -> str:
        return self._format_length_error(error.path, error.actual_value,
                                         error.min_length, "at least")

    def format_max_length_error(self, error: MaxLengthValidationError) -> str:
        return self._format_length_error(error.path, error.actual_value,
                                         error.max_length, "at most")

    def format_alphabet_error(self, error: AlphabetValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must contain only {error.alphabet!r}, but {error.actual_value!r} given")

    def format_substr_error(self, error: SubstrValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must contain {error.substr!r}, but {error.actual_value!r} given")

    def format_regex_error(self, error: RegexValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must match pattern {error.pattern!r}, but {error.actual_value!r} given")

    def format_missing_element_error(self, error: MissingElementValidationError) -> str:
        path = deepcopy(error.path)
        formatted_path = self._format_path(path[error.index])
        return f"Element {formatted_path} does not exist"

    def format_extra_element_error(self, error: ExtraElementValidationError) -> str:
        formatted_path = self._at_path(error.path)
        return f"Value{formatted_path} contains extra element at index {error.index!r}"

    def format_missing_key_error(self, error: MissingKeyValidationError) -> str:
        path = deepcopy(error.path)
        formatted_path = self._format_path(path[error.missing_key])
        return f"Key {formatted_path} does not exist"

    def format_extra_key_error(self, error: ExtraKeyValidationError) -> str:
        formatted_path = self._at_path(error.path)
        return f"Value{formatted_path} contains extra key {error.extra_key!r}"

    def format_schema_missmatch_error(self, error: SchemaMismatchValidationError) -> str:
        return self._format_schema_missmatch_error(error, schema_path=[])

    def _format_schema_missmatch_error(
        self,
        error: SchemaMismatchValidationError,
        schema_path: Optional[List[int]] = None
    ) -> str:
        if schema_path is None:
            schema_path = []
        if error.subschema_errors is None:
            actual_type = self._get_type(error.actual_value)
            formatted_path = self._at_path(error.path)
            return (f"Value {actual_type}{formatted_path} "
                    f"must match any of {error.expected_schemas!r}, but {error.actual_value!r} "
                    f"given")

        error_lines = []
        level = len(schema_path)
        prefix = "| - " * level
        for index, errors in enumerate(error.subschema_errors):
            new_schema_path = schema_path + [index + 1]
            schema_num = ".".join(map(str, new_schema_path))
            schema_desc = f"{prefix}Schema {schema_num}:"
            schema_errors = []
            for err in errors:
                if isinstance(err, SchemaMismatchValidationError):
                    nested = self._format_schema_missmatch_error(
                        err, schema_path=new_schema_path
                    ).split(os.linesep)
                    for i, line in enumerate(nested):
                        if i == 0:
                            schema_errors.append("| - " * (level + 1) + line)
                        else:
                            schema_errors.append(line)
                else:
                    schema_errors.append(("| - " * (level + 1)) + err.format(self))
            if schema_errors:
                error_lines.append(schema_desc)
                error_lines.extend(schema_errors)

        p = self._format_path(error.path)
        msg = f"Value at {p} does not match any of the allowed schemas:"
        lines = [msg] + error_lines

        result = [lines[0]]
        for line in lines[1:]:
            result.append("| - " + line)
        return os.linesep.join(result)

    def format_invalid_uuid_version_error(self, error: InvalidUUIDVersionValidationError) -> str:
        actual_type = self._get_type(error.actual_value)
        formatted_path = self._at_path(error.path)
        return (f"Value {actual_type}{formatted_path} "
                f"must be a UUID version {error.expected_version!r}, "
                f"but {error.actual_value!r} version {error.actual_version!r} given")
