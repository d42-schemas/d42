from typing import Any
from unittest.mock import sentinel

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema, substitute
from d42.declaration import GenericSchema
from d42.substitution.errors import SubstitutionError


@pytest.mark.parametrize(("value", "nested_sch"), [
    (None, schema.none),
    (True, schema.bool),
    (42, schema.int),
    (3.14, schema.float),
    ("banana", schema.str),
    ([], schema.list),
    ({}, schema.dict),
])
def test_any_substitution(value: Any, nested_sch: GenericSchema):
    with given:
        sch = schema.any

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.any(substitute(nested_sch, value))
        assert res != sch


def test_any_substitution_error():
    with given:
        sch = schema.any

    with when, raises(Exception) as exception:
        substitute(sch, sentinel)

    with then:
        assert exception.type is SubstitutionError


def test_any_value_substitution():
    with given:
        sch = schema.any(schema.str)

    with when:
        res = substitute(sch, "banana")

    with then:
        assert res == schema.any(schema.str("banana"))
        assert res != sch


def test_any_value_substitution_error():
    with given:
        sch = schema.any(schema.str)

    with when, raises(Exception) as exception:
        substitute(sch, 42)

    with then:
        assert exception.type is SubstitutionError


def test_any_values_substitution():
    with given:
        sch = schema.any(schema.str, schema.none)

    with when:
        res = substitute(sch, None)

    with then:
        assert res == schema.any(schema.none)
        assert res != sch


def test_any_values_substitution_error():
    with given:
        sch = schema.any(schema.str, schema.none)

    with when, raises(Exception) as exception:
        substitute(sch, 42)

    with then:
        assert exception.type is SubstitutionError


def test_any_nested_values_substitution():
    with given:
        sch = schema.any(schema.none, schema.any(schema.str, schema.none))

    with when:
        res = substitute(sch, None)

    with then:
        assert res == schema.any(schema.none, schema.any(schema.none))
        assert res != sch


def test_any_nested_values_substitution_error():
    with given:
        sch = schema.any(schema.none, schema.any(schema.str, schema.none))

    with when, raises(Exception) as exception:
        substitute(sch, 42)

    with then:
        assert exception.type is SubstitutionError


def test_any_dict_substitution():
    with given:
        sch = schema.any(
            schema.dict({
                "key": schema.str
            })
        )

    with when:
        res = substitute(sch, {"key": "..."})

    with then:
        assert res == schema.any(
            schema.dict({
                "key": schema.str("...")
            })
        )
        assert res != sch


def test_any_dict_substitution_error():
    with given:
        sch = schema.any(
            schema.dict({
                "key": schema.str
            })
        )

    with when, raises(Exception) as exception:
        substitute(sch, {"unknown": "..."})

    with then:
        assert exception.type is SubstitutionError
