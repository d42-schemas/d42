from typing import Any, Dict

import pytest
from baby_steps import given, then, when
from th import PathHolder

from d42 import optional, schema
from d42.validation import validate
from d42.validation.errors import ExtraKeyValidationError, TypeValidationError


@pytest.mark.parametrize("value", [
    {"id": 1},
    {"id": 1, "name": "Bob"},
])
def test_dict_with_optional_key_validation(value: Dict[Any, Any]):
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str,
        })

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_dict_with_optional_key_validation_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str,
        })

    with when:
        result = validate(sch, {
            "id": 1,
            "name": None
        })

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder()["name"], None, str)
        ]


def test_dict_relaxed_with_optional_key_validation_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str,
            ...: ...
        })

    with when:
        result = validate(sch, {
            "id": 1,
            "name": None
        })

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder()["name"], None, str)
        ]


def test_dict_extra_key_with_optional_validation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
            optional("created_at"): schema.str,
        })
        value = {
            "id": 1,
            "name": "Bob",
            "extra": "unexpected"
        }

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ExtraKeyValidationError(PathHolder(), value, "extra")
        ]
