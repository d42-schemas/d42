import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.representation import represent


def test_bytes_representation():
    with given:
        sch = schema.bytes

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes"


@pytest.mark.parametrize(
    ("value", "expected_repr"),
    [
        (b"", "schema.bytes(b'')"),
        (b"banana", "schema.bytes(b'banana')"),
    ]
)
def test_bytes_value_representation(value: bool, expected_repr: str):
    with given:
        sch = schema.bytes(value)

    with when:
        res = represent(sch)

    with then:
        assert res == expected_repr
