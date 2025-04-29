from typing import Any

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import (
    ExtraKeyValidationError,
    MissingKeyValidationError,
    SchemaMismatchValidationError,
)


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


def test_any_all_schemas_have_type_errors():
    with given:
        value = 42
        types = (schema.str, schema.none)

    with when:
        result = validate(schema.any(*types), value)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder(), value, types)
        ]


def test_any_one_schema_has_min_errors():
    with given:
        value = {"id": "42", "type": "banana"}
        BananaSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("banana"),
        })
        AppleSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("apple"),
        })

    with when:
        result = validate(schema.any(BananaSchema, AppleSchema), value)

    with then:
        assert not result.has_errors()


def test_any_multiple_schemas_have_min_errors():
    with given:
        value = {"id": "42", "type": "banana"}
        BananaSchema1 = schema.dict({
            "id": schema.str,
            "type": schema.str("banana"),
        })
        BananaSchema2 = schema.dict({
            "id": schema.str,
            "type": schema.str("banana"),
        })
        AppleSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("apple"),
        })

    with when:
        result = validate(schema.any(BananaSchema1, BananaSchema2, AppleSchema), value)

    with then:
        assert not result.has_errors()


def test_any_schema_with_extra_fields():
    with given:
        value = {"id": "42", "type": "banana", "extra": "field"}
        BananaSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("banana"),
        })
        AppleSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("apple"),
        })

    with when:
        result = validate(schema.any(BananaSchema, AppleSchema), value)

    with then:
        assert result.get_errors() == [
            ExtraKeyValidationError(PathHolder(), value, "extra")
        ]


def test_any_schema_with_missing_fields():
    with given:
        value = {"id": "42", "type": "banana"}
        BananaSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("banana"),
            "name": schema.str,
        })
        AppleSchema = schema.dict({
            "id": schema.str,
            "type": schema.str("apple"),
            "name": schema.str,
        })

    with when:
        result = validate(schema.any(BananaSchema, AppleSchema), value)

    with then:
        assert result.get_errors() == [
            MissingKeyValidationError(PathHolder(), value, "name")
        ]
