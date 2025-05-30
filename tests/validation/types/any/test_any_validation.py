from typing import Any

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import SchemaMismatchValidationError, TypeValidationError


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
            SchemaMismatchValidationError(
                PathHolder(),
                value,
                types,
                [(0, [TypeValidationError(PathHolder(), value, type(None))])]
            )
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
        p = PathHolder()
        e1 = TypeValidationError(p, value, int)
        e2 = TypeValidationError(p, value, str)
        errs = [(0, [e1]), (1, [e2])]

    with when:
        result = validate(schema.any(*types), value)

    with then:
        expected = SchemaMismatchValidationError(p, value, types, errs)
        assert result.get_errors() == [expected]


def test_any_type_validation_kwargs():
    with given:
        actual_value = False
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(schema.any(schema.none), actual_value, path=path)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(path, actual_value, (schema.none,),
                                          [(0, [TypeValidationError(path,
                                                                    actual_value, type(None))])])
        ]


def test_nested_any_validation_error():
    with given:
        value = 3.14

    with when:
        result = validate(schema.any(schema.none, schema.any(schema.str, schema.int)), value)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(
                PathHolder(),
                value,
                (schema.none, schema.str, schema.int),
                [
                    (0, [TypeValidationError(PathHolder(), value, type(None))]),
                    (1, [TypeValidationError(PathHolder(), value, str)]),
                    (2, [TypeValidationError(PathHolder(), value, int)])
                ]
            )
        ]
