from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_dict_relaxed_no_keys_substitution():
    with given:
        sch = schema.dict({...: ...})

    with when:
        res = substitute(sch, {})

    with then:
        assert res == schema.dict({...: ...})
        assert id(res) != id(sch)


def test_dict_relaxed_keys_substitution():
    with given:
        sch = schema.dict({...: ...})

    with when:
        res = substitute(sch, {
            "result": {
                "id": 1,
                "name": "Bob"
            },
        })

    with then:
        assert res == schema.dict({
            "result": schema.dict({
                "id": schema.int(1),
                "name": schema.str("Bob"),
            }),
            ...: ...
        })
        assert res != sch


def test_dict_relaxed_values_substitution():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
                ...: ...
            }),
            ...: ...
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
                ...: ...
            }),
            ...: ...
        })
        assert res != sch


def test_dict_relaxed_more_keys_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            ...: ...
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            "name": "Bob",
        })

    with then:
        assert exception.type is SubstitutionError


def test_dict_relaxed_les_keys_substitution():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
            ...: ...
        })

    with when:
        res = substitute(sch, {
            "id": 1,
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            "name": schema.str,
            ...: ...
        })
        assert res != sch


def test_dict_relaxed_value_substitution():
    with given:
        sch = schema.dict

    with when:
        res = substitute(sch, {
            "id": 1,
            ...: ...
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            ...: ...
        })
        assert res != sch


def test_relaxed_dict_relaxed_value_substitution():
    with given:
        sch = schema.dict({...: ...})

    with when:
        res = substitute(sch, {
            "id": 1,
            ...: ...
        })

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            ...: ...
        })
        assert res != sch


def test_dict_relaxed_value_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            ...: ...
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            ...: ...
        })

    with then:
        assert exception.type is SubstitutionError
