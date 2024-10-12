import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.representor import represent


def test_bool_representation():
    with given:
        sch = schema.bool

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bool"


@pytest.mark.parametrize(
    ("value", "expected_repr"),
    [
        (True, "schema.bool(True)"),
        (False, "schema.bool(False)"),
    ]
)
def test_bool_value_representation(value: bool, expected_repr: str):
    with given:
        sch = schema.bool(value)

    with when:
        res = represent(sch)

    with then:
        assert res == expected_repr
