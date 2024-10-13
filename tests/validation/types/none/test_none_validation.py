from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import TypeValidationError


def test_none_validation():
    with when:
        result = validate(schema.none, None)

    with then:
        assert result.get_errors() == []


def test_none_validation_error():
    with given:
        value = False

    with when:
        result = validate(schema.none, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, type(None))
        ]


def test_none_type_validation_kwargs():
    with given:
        actual_value = False
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.none, actual_value, path=path)

    with then:
        assert result.get_errors() == [
            TypeValidationError(path, actual_value, type(None))
        ]
