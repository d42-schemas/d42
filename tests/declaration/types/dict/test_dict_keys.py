from typing import KeysView

from baby_steps import given, then, when

from d42 import optional, schema


def test_dict_empty_keys():
    with given:
        sch = schema.dict

    with when:
        res = sch.keys()

    with then:
        assert res == KeysView([])


def test_dict_keys():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str,
            optional("email"): schema.str,
        })

    with when:
        res = sch.keys()

    with then:
        assert res == KeysView(["id", "name", "email"])
