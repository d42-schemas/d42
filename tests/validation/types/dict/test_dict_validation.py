from typing import Any, Dict

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import schema
from d42.validation import validate
from d42.validation.errors import (
    ExtraKeyValidationError,
    MissingKeyValidationError,
    TypeValidationError,
)


@pytest.mark.parametrize("value", [
    {},
    {"id": 1},
    {"id": 1, "name": "Bob"},
])
def test_dict_type_validation(value: Dict[Any, Any]):
    with given:
        sch = schema.dict

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_type_validation_error():
    with given:
        sch = schema.dict
        value = []

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, dict)]


def test_dict_no_keys_validation():
    with given:
        sch = schema.dict({})
        value = {}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_keys_validation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
        })
        value = {"id": 1, "name": "Bob"}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_extra_key_validation_error():
    with given:
        sch = schema.dict({})
        value = {"id": 1}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ExtraKeyValidationError(PathHolder(), value, "id")
        ]


def test_dict_missing_key_validation_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
        })
        value = {"id": 1}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingKeyValidationError(PathHolder(), value, "name")
        ]


@pytest.mark.parametrize("value", [
    {},
    {"id": 1},
    {"id": 1, "name": "Bob"},
])
def test_dict_relaxed_no_keys_validation(value: Dict[Any, Any]):
    with given:
        sch = schema.dict({...: ...})

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_relaxed_keys_validation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
            ...: ...,
        })
        value = {"id": 1, "name": "Bob", "is_deleted": False}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_nested_keys_validation():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
            })
        })
        value = {
            "result": {
                "id": 1,
                "name": "Bob"
            }
        }

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_nested_extra_key_validation_error():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
            })
        })
        value = {
            "result": {
                "id": 1,
                "name": "Bob",
            }
        }

    with when:
        result = validate(sch, value)

    with then:
        path = PathHolder()["result"]
        assert result.get_errors() == [
            ExtraKeyValidationError(path, value["result"], "name")
        ]


def test_dict_nested_missing_key_validation_error():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
            })
        })
        value = {
            "result": {
                "id": 1
            }
        }

    with when:
        result = validate(sch, value)

    with then:
        path = PathHolder()["result"]
        assert result.get_errors() == [
            MissingKeyValidationError(path, value["result"], "name")
        ]


def test_dict_validation_kwargs():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
        })
        value = {"id": 1}
        path = PathHolder().items[0]["key"]

    with when:
        result = validate(sch, value, path=path)

    with then:
        assert result.get_errors() == [
            MissingKeyValidationError(path, value, "name")
        ]
