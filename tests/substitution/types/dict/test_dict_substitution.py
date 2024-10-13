from unittest.mock import sentinel

from baby_steps import given, then, when
from pytest import raises

from d42 import optional, schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError
from d42.utils import from_native


def test_dict_no_keys_substitution():
    with given:
        sch = schema.dict

    with when:
        res = substitute(sch, {})

    with then:
        assert res == schema.dict({})
        assert res != sch


def test_dict_invalid_value_substitution_error():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        substitute(sch, [])

    with then:
        assert exception.type is SubstitutionError


def test_dict_keys_substitution():
    with given:
        sch = schema.dict
        value = {
            "result": {
                "id": 1,
                "name": "Bob"
            },
        }

    with when:
        res = substitute(sch, value)

    with then:
        assert res == from_native(value)
        assert res != sch


def test_dict_value_substitution_error():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        substitute(sch, {"val": sentinel})

    with then:
        assert exception.type is SubstitutionError


def test_dict_values_substitution():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
            }),
        })

    with when:
        res = substitute(sch, {
            "result": {
                "id": 1,
                "name": "Bob",
            },
        })

    with then:
        assert res == schema.dict({
            "result": schema.dict({
                "id": schema.int(1),
                "name": schema.str("Bob"),
            }),
        })
        assert res != sch


def test_dict_incorrect_value_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {"id": "1"})

    with then:
        assert exception.type is SubstitutionError


def test_dict_incorrect_key_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {"identifier": 42})

    with then:
        assert exception.type is SubstitutionError


def test_dict_more_keys_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            "name": "Bob",
        })

    with then:
        assert exception.type is SubstitutionError


def test_dict_less_keys_substitution():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
            }),
        })

    with when:
        res = substitute(sch, {
            "result": {
                "id": 1,
            },
        })

    with then:
        assert res == schema.dict({
            "result": schema.dict({
                "id": schema.int(1),
                "name": schema.str,
            }),
        })
        assert res != sch


def test_dict_nested_less_keys_substitution():
    with given:
        sch = schema.dict({
            "friends": schema.list(schema.dict({
                "id": schema.int,
                "name": schema.str,
            }))
        })

    with when:
        res = substitute(sch, {
            "friends": [
                {
                    "id": 1
                }
            ]
        })

    with then:
        assert res == schema.dict({
            "friends": schema.list([
                schema.dict({
                    "id": schema.int(1),
                    "name": schema.str,
                })
            ])
        })
        assert res != sch


def test_dict_incorrect_nested_key_substitution_error():
    with given:
        sch = schema.dict({
            "res": schema.dict({
                "id": schema.int,
            })
        })

    with when, raises(Exception) as exception:
        substitute(sch, {"identifier": {"id": 42}})

    with then:
        assert exception.type is SubstitutionError


def test_dict_with_optional_key_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str
        })

    with when:
        res = substitute(sch, {
            "id": 1,
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            optional("name"): schema.str
        })
        assert res != sch


def test_dict_with_optional_key_override_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str
        })

    with when:
        res = substitute(sch, {
            "id": 1,
            "name": "Bob"
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            "name": schema.str("Bob"),
        })
        assert res != sch


def test_dict_with_optional_key_invalid_type_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            "name": None
        })

    with then:
        assert exception.type is SubstitutionError


def test_dict_with_optional_key_ellipsis_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str.len(1, ...)
        })

    with when:
        res = substitute(sch, {
            "id": 1,
            "name": ...
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            "name": schema.str.len(1, ...),
        })
        assert res != sch


def test_dict_ellipsis_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str.len(1, ...)
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            ...: ...
        })

    with then:
        assert exception.type is SubstitutionError
