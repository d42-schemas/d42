from baby_steps import given, then, when

from d42 import schema


def test_any_iterable():
    with given:
        sch = schema.any(schema.str, schema.none)

    with when:
        res = [x for x in sch]

    with then:
        assert res == [schema.str, schema.none]


def test_any_iterable_empty():
    with given:
        sch = schema.any

    with when:
        res = [x for x in sch]

    with then:
        assert res == []


def test_any_iterable_nested():
    with given:
        sch = schema.any(schema.any(schema.str, schema.int), schema.none)

    with when:
        res = [x for x in sch]

    with then:
        assert res == [schema.str, schema.int, schema.none]
