from datetime import datetime, timedelta

from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import TypeValidationError, ValueValidationError


def test_datetime_type_validation():
    with given:
        value = datetime.now()

    with when:
        result = validate(schema.datetime, value)

    with then:
        assert result.get_errors() == []


def test_datetime_type_validation_error():
    with given:
        value = str(datetime.now())

    with when:
        result = validate(schema.datetime, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, datetime)]


def test_datetime_value_validation():
    with given:
        value = datetime.now()

    with when:
        result = validate(schema.datetime(value), value)

    with then:
        assert result.get_errors() == []


def test_datetime_value_validation_error():
    with given:
        expected_value = datetime.now()
        actual_value = datetime.now() + timedelta(days=1)

    with when:
        result = validate(schema.datetime(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value)
        ]


def test_datetime_type_validation_kwargs():
    with given:
        expected_value = datetime.now()
        actual_value = datetime.now() + timedelta(days=1)
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.datetime(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]
