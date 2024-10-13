from typing import Any, List

from d42.declaration import GenericSchema, Schema

from ._abstract_formatter import AbstractFormatter
from ._formatter import Formatter
from ._validation_result import ValidationResult
from ._validator import Validator

__all__ = ("validate", "validate_or_fail", "eq", "format_result",
           "Validator", "ValidationResult", "ValidationException",
           "Formatter", "AbstractFormatter",)


_validator = Validator()
_formatter = Formatter()


def validate(schema: GenericSchema, value: Any, **kwargs: Any) -> ValidationResult:
    return schema.__accept__(_validator, value=value, **kwargs)


class ValidationException(Exception):
    pass


def validate_or_fail(schema: GenericSchema, value: Any, **kwargs: Any) -> bool:
    result = validate(schema, value, **kwargs)
    errors = [e.format(_formatter) for e in result.get_errors()]
    if len(errors) == 0:
        return True
    message = "\n - " + "\n - ".join(errors)
    raise ValidationException(message)


def eq(schema: GenericSchema, value: Any) -> bool:
    if isinstance(value, Schema):
        return isinstance(value, schema.__class__) and (schema.props == value.props)
    return not validate(schema, value=value).has_errors()


def format_result(result: ValidationResult, formatter: Formatter = _formatter) -> List[str]:
    if not result.has_errors():
        return []
    errors = ["- " + e.format(formatter) for e in result.get_errors()]
    return ["valera.ValidationException"] + errors


Schema.__override__(Schema.__eq__.__name__, eq)
