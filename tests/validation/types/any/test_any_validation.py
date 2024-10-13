from typing import Any

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema, validate
from d42.validation.errors import SchemaMismatchValidationError


@pytest.mark.parametrize("value", [
    None,
    True,
    42,
    3.14,
    "banana",
    [],
    {},
    Exception,
])
def test_any_validation(value: Any):
    with when:
        result = validate(schema.any, value)

    with then:
        assert result.get_errors() == []


def test_any_type_validation():
    with when:
        result = validate(schema.any(schema.none), None)

    with then:
        assert result.get_errors() == []


def test_any_type_validation_error():
    with given:
        value = False
        types = (schema.none,)

    with when:
        result = validate(schema.any(*types), value)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder(), value, types)
        ]


@pytest.mark.parametrize("value", [42, "42"])
def test_any_types_validation(value: Any):
    with when:
        result = validate(schema.any(schema.int, schema.str), value)

    with then:
        assert result.get_errors() == []


def test_any_types_validation_error():
    with given:
        value = None
        types = (schema.int, schema.str)

    with when:
        result = validate(schema.any(*types), value)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder(), value, types)
        ]


def test_any_type_validation_kwargs():
    with given:
        actual_value = False
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.any(schema.none), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(path, actual_value, (schema.none,))
        ]
