from baby_steps import given, then, when
from th import PathHolder

from d42 import schema, validate
from d42.validation.errors import TypeValidationError, ValueValidationError


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


def test_bool_type_validation_kwargs():
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
