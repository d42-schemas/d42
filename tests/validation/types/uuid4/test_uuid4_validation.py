import uuid
from uuid import UUID, uuid4, uuid5

from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import (
    InvalidUUIDVersionValidationError,
    TypeValidationError,
    ValueValidationError,
)


def test_uuid4_type_validation():
    with when:
        result = validate(schema.uuid4, uuid4())

    with then:
        assert result.get_errors() == []


def test_uuid4_type_validation_error():
    with given:
        value = str(uuid4())

    with when:
        result = validate(schema.uuid4, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, UUID)]


def test_uuid4_value_validation():
    with given:
        value = uuid4()

    with when:
        result = validate(schema.uuid4(value), value)

    with then:
        assert result.get_errors() == []


def test_uuid4_value_validation_error():
    with given:
        expected_value = uuid4()
        actual_value = uuid4()

    with when:
        result = validate(schema.uuid4(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value)
        ]


def test_uuid4_version_validation_error():
    with given:
        expected_value = uuid4()
        actual_value = uuid5(uuid.NAMESPACE_DNS, "python.org")

    with when:
        result = validate(schema.uuid4(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            InvalidUUIDVersionValidationError(PathHolder(), actual_value,
                                              actual_value.version, expected_value.version),
        ]


def test_uuid_type_validation_kwargs():
    with given:
        expected_value = uuid4()
        actual_value = uuid4()
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.uuid4(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]
