from copy import deepcopy
from typing import Any

from niltype import Nil, Nilable
from th import PathHolder

from d42.declaration import is_ellipsis
from d42.declaration.types import DictSchema, ListSchema
from d42.validation import ValidationResult, Validator
from d42.validation.errors import (
    ExtraKeyValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MinLengthValidationError,
)

__all__ = ("SubstitutorValidator",)


class SubstitutorValidator(Validator):
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

        if (schema.props.type is Nil) and (schema.props.elements is Nil):
            return result

        if schema.props.type is not Nil:
            type_schema = schema.props.type
            for index, elem in enumerate(value):
                if is_ellipsis(elem) and (index == 0 or index == len(value) - 1):
                    continue
                nested_path = deepcopy(path)[index]
                res = type_schema.__accept__(self, value=elem, path=nested_path, **kwargs)
                result.add_errors(res.get_errors())
            return result
        else:
            return super().visit_list(schema, value=value, path=path, **kwargs)

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
                if is_ellipsis(value[key]):
                    continue
                nested_path = deepcopy(path)[key]
                res = val.__accept__(self, value=value[key], path=nested_path, **kwargs)
                result.add_errors(res.get_errors())

        if (... not in schema.props.keys) and (set(schema.props.keys) != set(value)):
            for key, val in value.items():
                if key not in schema.props.keys:
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result
