import re
from copy import deepcopy
from datetime import date, datetime
from math import isclose
from typing import Any, Callable, List, Optional, Type, cast
from uuid import UUID

from niltype import Nil, Nilable
from th import PathHolder

from d42.declaration import GenericSchema, SchemaVisitor
from d42.declaration.types import (
    AnySchema,
    BoolSchema,
    BytesSchema,
    DateSchema,
    DateTimeSchema,
    DictSchema,
    FloatSchema,
    GenericTypeAliasSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    TypeAliasPropsType,
    UUID4Schema,
)
from d42.utils import is_ellipsis

from ._validation_result import ValidationResult
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
    UniqueValidationError,
    ValidationError,
    ValueValidationError,
)

__all__ = ("Validator",)

from ..generation._generator import UniqueSet


class Validator(SchemaVisitor[ValidationResult]):
    def __init__(self, *,
                 validation_result_factory: Callable[[], ValidationResult] = ValidationResult,
                 path_holder_factory: Callable[[], PathHolder] = PathHolder) -> None:
        self._validation_result_factory = validation_result_factory
        self._path_holder_factory = path_holder_factory

    def make_validation_result(self) -> ValidationResult:
        return self._validation_result_factory()

    def make_path(self) -> PathHolder:
        return self._path_holder_factory()

    def _validate_type(self, path: PathHolder, value: Any,
                       expected_type: Type[Any]) -> Optional[ValidationError]:
        if not isinstance(value, expected_type):
            return TypeValidationError(path, value, expected_type)
        return None

    def _validate_value(self, path: PathHolder, value: Any,
                        expected_val: Any) -> Optional[ValidationError]:
        if value != expected_val:
            return ValueValidationError(path, value, expected_val)
        return None

    def _validate_elements(self,
                           path: PathHolder,
                           value: List[Any],
                           elements: List[GenericSchema],
                           start: int = 0,
                           **kwargs: Any) -> List[ValidationError]:
        errors: List[ValidationError] = []
        for index, element_schema in enumerate(elements):
            real_index = start + index
            try:
                val = value[real_index]
            except IndexError:
                errors.append(MissingElementValidationError(path, value, real_index))
                break
            else:
                nested_path = deepcopy(path)[real_index]
                res = element_schema.__accept__(self, value=val, path=nested_path, **kwargs)
                errors += res.get_errors()
        return errors

    def visit(self, schema: GenericSchema, *, value: Any = Nil, path: Nilable[PathHolder] = Nil,
              **kwargs: Any) -> ValidationResult:
        if validate_method := getattr(schema, "__d42_validate__", None):
            return cast(ValidationResult, validate_method(self, value=value, path=path, **kwargs))
        raise NotImplementedError(f"{schema.__class__.__name__} has no method '__d42_validate__'")

    def visit_none(self, schema: NoneSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, type(None)):
            return result.add_error(error)

        return result

    def visit_bool(self, schema: BoolSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, bool):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result

    def visit_int(self, schema: IntSchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, int):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        if schema.props.min is not Nil:
            if value < schema.props.min:
                result.add_error(MinValueValidationError(path, value, schema.props.min))

        if schema.props.max is not Nil:
            if value > schema.props.max:
                result.add_error(MaxValueValidationError(path, value, schema.props.max))

        return result

    def visit_float(self, schema: FloatSchema, *,
                    value: Any = Nil, path: Nilable[PathHolder] = Nil,
                    **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, float):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if schema.props.precision is Nil:
                if not isclose(value, schema.props.value):
                    return result.add_error(ValueValidationError(path, value, schema.props.value))
            else:
                scale_factor = 10 ** schema.props.precision
                scaled_actual = round(value * scale_factor)
                scaled_expected = round(schema.props.value * scale_factor)
                if not isclose(scaled_expected, scaled_actual, rel_tol=0, abs_tol=0):
                    return result.add_error(ValueValidationError(path, value, schema.props.value))

        if schema.props.min is not Nil:
            if value < schema.props.min:
                result.add_error(MinValueValidationError(path, value, schema.props.min))

        if schema.props.max is not Nil:
            if value > schema.props.max:
                result.add_error(MaxValueValidationError(path, value, schema.props.max))

        return result

    def visit_str(self, schema: StrSchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> Any:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, str):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        if schema.props.pattern is not Nil:
            match_object = re.search(schema.props.pattern, value)
            if match_object is None:
                error = RegexValidationError(path, value, schema.props.pattern)
                return result.add_error(error)

        if schema.props.len is not Nil:
            if len(value) != schema.props.len:
                result.add_error(LengthValidationError(path, value, schema.props.len))
        if schema.props.min_len is not Nil:
            if len(value) < schema.props.min_len:
                result.add_error(MinLengthValidationError(path, value, schema.props.min_len))
        if schema.props.max_len is not Nil:
            if len(value) > schema.props.max_len:
                result.add_error(MaxLengthValidationError(path, value, schema.props.max_len))

        if schema.props.substr is not Nil:
            if schema.props.substr not in value:
                result.add_error(SubstrValidationError(path, value, schema.props.substr))

        if schema.props.alphabet is not Nil:
            alphabet = set(schema.props.alphabet)
            for letter in value:
                if letter not in alphabet:
                    return result.add_error(
                        AlphabetValidationError(PathHolder(), value, schema.props.alphabet))

        return result

    def visit_list(self, schema: ListSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, list):
            return result.add_error(error)

        if schema.props.len is not Nil:
            if len(value) != schema.props.len:
                return result.add_error(LengthValidationError(path, value, schema.props.len))
        if schema.props.min_len is not Nil:
            if len(value) < schema.props.min_len:
                return result.add_error(
                    MinLengthValidationError(path, value, schema.props.min_len))
        if schema.props.max_len is not Nil:
            if len(value) > schema.props.max_len:
                return result.add_error(
                    MaxLengthValidationError(path, value, schema.props.max_len))

        if schema.props.unique and not self._is_unique_list(value):
            result.add_error(UniqueValidationError(path, value))
            return result

        if (schema.props.type is Nil) and (schema.props.elements is Nil):
            return result

        if schema.props.type is not Nil:
            type_schema = schema.props.type
            for index, elem in enumerate(value):
                nested_path = deepcopy(path)[index]
                res = type_schema.__accept__(self, value=elem, path=nested_path, **kwargs)
                result.add_errors(res.get_errors())
            return result

        elements = cast(List[GenericSchema], schema.props.elements)

        # body
        if (len(elements) > 2) and is_ellipsis(elements[0]) and is_ellipsis(elements[-1]):
            if len(value) == 0:
                errors = self._validate_elements(path, value, elements[1:-1], **kwargs)
                return result.add_errors(errors)
            all_errors = []
            for index, val in enumerate(value):
                errors = self._validate_elements(path, value, elements[1:-1], index, **kwargs)
                all_errors.append(errors)
            all_errors.sort(key=len)
            return result.add_errors(all_errors[0])

        # head
        if (len(elements) >= 2) and is_ellipsis(elements[-1]):
            errors = self._validate_elements(path, value, elements[:-1], **kwargs)
            return result.add_errors(errors)

        # tail
        if (len(elements) >= 1) and is_ellipsis(elements[0]):
            elements = elements[1:]
            start = max(0, len(value) - len(elements))
            errors = self._validate_elements(path, value, elements, start, **kwargs)
            return result.add_errors(errors)

        errors = self._validate_elements(path, value, elements, **kwargs)
        result.add_errors(errors)
        if len(value) > len(elements):
            for index in range(len(elements), len(value)):
                result.add_error(ExtraElementValidationError(path, value, index))

        return result

    def _is_unique_list(self, items: List[Any]) -> bool:
        if not items:
            return True

        unique_items = UniqueSet()

        for item in items:
            if item in unique_items:
                return False
            unique_items.add(item)

        return True

    def visit_dict(self, schema: DictSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, dict):
            return result.add_error(error)

        if schema.props.keys is Nil:
            return result

        for key, (val, is_optional) in schema.props.keys.items():
            if is_ellipsis(key):
                continue
            if key in value:
                nested_path = deepcopy(path)[key]
                res = val.__accept__(self, value=value[key], path=nested_path, **kwargs)
                result.add_errors(res.get_errors())
            else:
                if not is_optional:
                    result.add_error(MissingKeyValidationError(path, value, key))

        if (... not in schema.props.keys):
            for key, val in value.items():
                if key not in schema.props.keys:
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result

    def visit_any(self, schema: AnySchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if schema.props.types is Nil:
            return result

        for sch_type in schema.props.types:
            res = sch_type.__accept__(self, path=path, value=value, **kwargs)
            if not res.has_errors():
                return result

        result.add_error(SchemaMismatchValidationError(path, value, schema.props.types))
        return result

    def visit_bytes(self, schema: BytesSchema, *,
                    value: Any = Nil, path: Nilable[PathHolder] = Nil,
                    **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, bytes):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result

    def visit_type_alias(self, schema: GenericTypeAliasSchema[TypeAliasPropsType], *,
                         value: Any = Nil, path: Nilable[PathHolder] = Nil,
                         **kwargs: Any) -> ValidationResult:
        return schema.props.type.__accept__(self, value=value, path=path, **kwargs)

    def visit_datetime(self, schema: DateTimeSchema, *,
                       value: Any = Nil, path: Nilable[PathHolder] = Nil,
                       **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, datetime):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result

    def visit_uuid4(self, schema: UUID4Schema, *,
                    value: Any = Nil, path: Nilable[PathHolder] = Nil,
                    **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, UUID):
            return result.add_error(error)

        if value.version != 4:
            return result.add_error(
                InvalidUUIDVersionValidationError(path, value, value.version, 4))

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result

    def visit_date(self, schema: DateSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, date):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result
