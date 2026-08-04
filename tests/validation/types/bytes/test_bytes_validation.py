import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import (
    LengthValidationError,
    MaxLengthValidationError,
    MinLengthValidationError,
    TypeValidationError,
    ValueValidationError,
)


def test_bytes_type_validation():
    with when:
        result = validate(schema.bytes, b"banana")

    with then:
        assert result.get_errors() == []


def test_bytes_type_validation_error():
    with given:
        value = "banana"

    with when:
        result = validate(schema.bytes, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, bytes),
        ]


def test_bytes_value_validation():
    with given:
        value = b"banana"

    with when:
        result = validate(schema.bytes(value), value)

    with then:
        assert result.get_errors() == []


def test_bytes_value_validation_error():
    with given:
        expected_value = b"banana"
        actual_value = b"cucumber"

    with when:
        result = validate(schema.bytes(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value),
        ]


def test_bytes_type_validation_kwargs():
    with given:
        expected_value = b"banana"
        actual_value = b"cucumber"
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.bytes(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]


def test_bytes_len_validation():
    with given:
        value = b"banana"

    with when:
        result = validate(schema.bytes.len(6), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize("value", [
    b"banana",
    b"banana!!",
])
def test_bytes_len_validation_error(value: bytes):
    with given:
        length = 7

    with when:
        result = validate(schema.bytes.len(length), value)

    with then:
        assert result.get_errors() == [
            LengthValidationError(PathHolder(), value, length),
        ]


@pytest.mark.parametrize("value", [
    b"banana",
    b"banana!",
])
def test_bytes_min_len_validation(value: bytes):
    with when:
        result = validate(schema.bytes.len(6, ...), value)

    with then:
        assert result.get_errors() == []


def test_bytes_min_len_validation_error():
    with given:
        value = b"banana"
        min_length = 7

    with when:
        result = validate(schema.bytes.len(min_length, ...), value)

    with then:
        assert result.get_errors() == [
            MinLengthValidationError(PathHolder(), value, min_length),
        ]


@pytest.mark.parametrize("value", [
    b"banana",
    b"banana!",
])
def test_bytes_max_len_validation(value: bytes):
    with when:
        result = validate(schema.bytes.len(..., 7), value)

    with then:
        assert result.get_errors() == []


def test_bytes_max_len_validation_error():
    with given:
        value = b"banana"
        max_length = 5

    with when:
        result = validate(schema.bytes.len(..., max_length), value)

    with then:
        assert result.get_errors() == [
            MaxLengthValidationError(PathHolder(), value, max_length),
        ]


@pytest.mark.parametrize(("min_length", "max_length"), [
    (6, 6),
    (5, 7),
])
def test_bytes_min_max_len_validation(min_length: int, max_length: int):
    with given:
        value = b"banana"

    with when:
        result = validate(schema.bytes.len(min_length, max_length), value)

    with then:
        assert result.get_errors() == []


@pytest.mark.parametrize(("min_length", "max_length"), [
    (5, 5),
    (7, 7),
])
def test_bytes_min_max_len_validation_error(
    min_length: int,
    max_length: int,
):
    with given:
        value = b"banana"

    with when:
        result = validate(schema.bytes.len(min_length, max_length), value)

    with then:
        assert len(result.get_errors()) == 1
