from baby_steps import given, then, when

from d42 import schema
from d42.representor import represent


def test_list_of_representation():
    with given:
        sch = schema.list(schema.bool)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.bool)"


def test_list_of_values_representation():
    with given:
        sch = schema.list(schema.int(1))

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.int(1))"


def test_list_of_repr_values_representation():
    with given:
        sch = schema.list(schema.str("banana"))

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.str('banana'))"


def test_list_of_len_representation():
    with given:
        sch = schema.list(schema.int).len(10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.int).len(10)"


def test_list_of_min_len_representation():
    with given:
        sch = schema.list(schema.int).len(1, ...)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.int).len(1, ...)"


def test_list_of_max_len_representation():
    with given:
        sch = schema.list(schema.int).len(..., 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.int).len(..., 10)"


def test_list_of_min_max_len_representation():
    with given:
        sch = schema.list(schema.int).len(1, 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list(schema.int).len(1, 10)"
