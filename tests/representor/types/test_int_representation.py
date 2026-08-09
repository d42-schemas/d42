import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.representation import represent


def test_int_representation():
    with given:
        sch = schema.int

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.int"


@pytest.mark.parametrize(
    ("value", "expected_repr"),
    [
        (42, "schema.int(42)"),
        (0, "schema.int(0)"),
        (-42, "schema.int(-42)"),
    ]
)
def test_int_value_representation(value: int, expected_repr: str):
    with given:
        sch = schema.int(value)

    with when:
        res = represent(sch)

    with then:
        assert res == expected_repr


def test_int_min_value_representation():
    with given:
        sch = schema.int.min(42)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.int.min(42)"


def test_int_max_value_representation():
    with given:
        sch = schema.int.max(42)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.int.max(42)"


def test_int_min_max_value_representation():
    with given:
        sch = schema.int.min(1).max(2)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.int.min(1).max(2)"


def test_int_min_max_with_value_representation():
    with given:
        sch = schema.int(2).min(1).max(3)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.int(2).min(1).max(3)"


def test_int_multiple_of_representation():
    with given:
        sch = schema.int.multiple_of(10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.int.multiple_of(10)"
