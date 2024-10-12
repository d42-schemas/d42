from baby_steps import given, then, when
from pytest import raises

from d42 import optional, schema


def test_dict_get_item():
    with given:
        id_sch = schema.int
        sch = schema.dict({"id": id_sch})

    with when:
        res = sch["id"]

    with then:
        assert res == id_sch


def test_dict_get_optinal_item():
    with given:
        id_sch = schema.int
        sch = schema.dict({optional("id"): id_sch})

    with when:
        res = sch["id"]

    with then:
        assert res == id_sch


def test_dict_get_nested_item():
    with given:
        id_sch = schema.int
        sch = schema.dict({
            "result": schema.dict({
                "id": id_sch
            })
        })

    with when:
        res = sch["result"]["id"]

    with then:
        assert res == id_sch


def test_dict_no_keys_get_nonexisting_item_error():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        sch["id"]

    with then:
        assert exception.type is KeyError
        assert str(exception.value) == "'id'"


def test_dict_get_nonexisting_item_error():
    with given:
        sch = schema.dict({})

    with when, raises(Exception) as exception:
        sch["id"]

    with then:
        assert exception.type is KeyError
        assert str(exception.value) == "'id'"


def test_dict_get_relaxed_item_error():
    with given:
        sch = schema.dict({...: ...})

    with when, raises(Exception) as exception:
        sch[...]

    with then:
        assert exception.type is KeyError
        assert str(exception.value) == "'...'"
