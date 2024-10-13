from baby_steps import given, then, when

from d42 import optional, schema


def test_dict_iterable():
    with given:
        sch = schema.dict({
            "id": schema.int.min(1),
            "name": schema.str.len(1, ...),
        })

    with when:
        res = [x for x in sch]

    with then:
        assert res == ["id", "name"]


def test_dict_iterable_optional():
    with given:
        sch = schema.dict({
            "id": schema.int.min(1),
            optional("name"): schema.str.len(1, ...),
        })

    with when:
        res = [x for x in sch]

    with then:
        assert res == ["id", "name"]


def test_dict_iterable_empty():
    with given:
        sch = schema.dict

    with when:
        res = [x for x in sch]

    with then:
        assert res == []
