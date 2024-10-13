import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import (
    MaxValueValidationError,
    MinValueValidationError,
    TypeValidationError,
    ValueValidationError,
)


def test_float_type_validation():
    with when:
        result = validate(schema.float, 3.14)

    with then:
        assert result.get_errors() == []


def test_float_type_validation_error():
    with given:
        value = 42

    with when:
        result = validate(schema.float, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, float)]


def test_float_value_validation():
    with given:
        value = 3.14

    with when:
        result = validate(schema.float(value), value)

    with then:
        assert result.get_errors() == []


def test_float_value_validation_error():
    with given:
        expected_value = 3.14
        actual_value = 3.15

    with when:
        result = validate(schema.float(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value)
        ]


@pytest.mark.parametrize("value", [3.15, 3.14])
def test_float_min_value_validation(value: float):
    with when:
        result = validate(schema.float.min(3.14), value)

    with then:
        assert result.get_errors() == []


def test_float_min_value_validation_error():
    with given:
        min_value = 3.14
        actual_value = 3.13

    with when:
        result = validate(schema.float.min(min_value), actual_value)

    with then:
        assert result.get_errors() == [
            MinValueValidationError(PathHolder(), actual_value, min_value)
        ]


@pytest.mark.parametrize("value", [3.14, 3.13])
def test_float_max_value_validation(value: float):
    with when:
        result = validate(schema.float.max(3.14), value)

    with then:
        assert result.get_errors() == []


def test_float_max_value_validation_error():
    with given:
        max_value = 3.14
        actual_value = 3.15

    with when:
        result = validate(schema.float.max(max_value), actual_value)

    with then:
        assert result.get_errors() == [
            MaxValueValidationError(PathHolder(), actual_value, max_value)
        ]


@pytest.mark.parametrize("value", [3.13, 3.14, 3.15])
def test_float_min_max_value_validation(value: float):
    with when:
        result = validate(schema.float.min(3.13).max(3.15), value)

    with then:
        assert result.get_errors() == []


def test_float_min_max_greater_value_validation_error():
    with given:
        min_value = 3.13
        max_value = 3.15
        actual_value = 3.16

    with when:
        result = validate(schema.float.min(min_value).max(max_value), actual_value)

    with then:
        assert result.get_errors() == [
            MaxValueValidationError(PathHolder(), actual_value, max_value)
        ]


def test_float_min_max_less_value_validation_error():
    with given:
        min_value = 3.13
        max_value = 3.15
        actual_value = 3.12

    with when:
        result = validate(schema.float.min(min_value).max(max_value), actual_value)

    with then:
        assert result.get_errors() == [
            MinValueValidationError(PathHolder(), actual_value, min_value)
        ]


def test_float_type_validation_kwargs():
    with given:
        expected_value = 3.14
        actual_value = 3.15
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.float(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]


@pytest.mark.parametrize("value", [-3.14, 3.0, 3.1, 3.14])
def test_float_precision_validation(value: float):
    with given:
        precision = 3

    with when:
        result = validate(schema.float.precision(precision), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [9.00, 9.001, 9.004])
def test_float_pos_value_with_precision_validation(value: float):
    with given:
        sch = schema.float(9.00).precision(2)

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [-9.00, -9.001, -9.004])
def test_float_neg_value_with_precision_validation(value: float):
    with given:
        sch = schema.float(-9.00).precision(2)

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [9.005, 9.01, -9.00])
def test_float_pos_value_with_precision_validation_error(value: float):
    with given:
        sch = schema.float(9.00).precision(2)

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), value, 9.00)
        ]


@pytest.mark.parametrize("value", [9.005, 9.01, -9.00])
def test_float_neg_value_with_precision_validation_error(value: float):
    with given:
        sch = schema.float(9.00).precision(2)

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), value, 9.00)
        ]
