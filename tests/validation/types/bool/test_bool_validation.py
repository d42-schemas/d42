import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import TypeValidationError, ValueValidationError


@pytest.mark.parametrize("value", [True, False])
def test_bool_type_validation(value: bool):
    with when:
        result = validate(schema.bool, value)

    with then:
        assert result.get_errors() == []


def test_bool_type_validation_error():
    with given:
        value = "True"

    with when:
        result = validate(schema.bool, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, bool)]


@pytest.mark.parametrize("value", [True, False])
def test_bool_value_validation(value: bool):
    with when:
        result = validate(schema.bool(value), value)

    with then:
        assert result.get_errors() == []


def test_bool_value_validation_error():
    with given:
        expected_value = True
        actual_value = False

    with when:
        result = validate(schema.bool(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value)
        ]


def test_bool_type_validation_kwargs():
    with given:
        expected_value = True
        actual_value = False
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.bool(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]
