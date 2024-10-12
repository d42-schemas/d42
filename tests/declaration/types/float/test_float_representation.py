import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.representor import represent


def test_float_representation():
    with given:
        sch = schema.float

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float"


@pytest.mark.parametrize(
    ("value", "expected_repr"),
    [
        (3.14, "schema.float(3.14)"),
        (0.0, "schema.float(0.0)"),
        (-3.14, "schema.float(-3.14)"),
    ]
)
def test_float_value_representation(value: float, expected_repr: str):
    with given:
        sch = schema.float(value)

    with when:
        res = represent(sch)

    with then:
        assert res == expected_repr


def test_float_min_value_representation():
    with given:
        sch = schema.float.min(3.14)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float.min(3.14)"


def test_float_max_value_representation():
    with given:
        sch = schema.float.max(3.14)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float.max(3.14)"


def test_float_precision_value_representation():
    with given:
        sch = schema.float.precision(3)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float.precision(3)"


def test_float_min_precision_value_representation():
    with given:
        sch = schema.float.min(3.14).precision(3)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float.min(3.14).precision(3)"


def test_float_min_max_precision_value_representation():
    with given:
        sch = schema.float.min(3.14).max(3.15).precision(3)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float.min(3.14).max(3.15).precision(3)"


def test_float_min_max_value_representation():
    with given:
        sch = schema.float.min(3.14).max(3.15)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float.min(3.14).max(3.15)"


def test_float_min_max_with_value_representation():
    with given:
        sch = schema.float(3.14).min(3.13).max(3.15)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.float(3.14).min(3.13).max(3.15)"
