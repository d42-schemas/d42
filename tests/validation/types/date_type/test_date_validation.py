from datetime import date, timedelta

from baby_steps import given, then, when
from th import PathHolder

from d42 import schema, validate
from d42.validation.errors import TypeValidationError, ValueValidationError


def test_date_type_validation():
    with given:
        value = date.today()

    with when:
        result = validate(schema.date, value)

    with then:
        assert result.get_errors() == []


def test_date_type_validation_error():
    with given:
        value = str(date.today())

    with when:
        result = validate(schema.date, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, date)]


def test_date_value_validation():
    with given:
        value = date.today()

    with when:
        result = validate(schema.date(value), value)

    with then:
        assert result.get_errors() == []


def test_date_value_validation_error():
    with given:
        expected_value = date.today()
        actual_value = date.today() + timedelta(days=1)

    with when:
        result = validate(schema.date(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value)
        ]


def test_date_type_validation_kwargs():
    with given:
        expected_value = date.today()
        actual_value = date.today() + timedelta(days=1)
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.date(expected_value), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            ValueValidationError(path, actual_value, expected_value)
        ]
