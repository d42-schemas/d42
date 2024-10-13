from baby_steps import given, then, when
from th import PathHolder

from d42.validation import ValidationResult, format_result
from d42.validation.errors import TypeValidationError


def test_format_result():
    with given:
        error = TypeValidationError(PathHolder(), "banana", int)
        result = ValidationResult([error])

    with when:
        formatted = format_result(result)

    with then:
        assert formatted == [
            "valera.ValidationException",
            "- Value 'banana' must be <class 'int'>, but <class 'str'> given",
        ]


def test_format_result_no_errors():
    with given:
        result = ValidationResult([])

    with when:
        formatted = format_result(result)

    with then:
        assert formatted == []
