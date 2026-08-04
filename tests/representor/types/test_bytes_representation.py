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
    ],
)
def test_bytes_value_representation(value: bytes, expected_repr: str):
    with given:
        sch = schema.bytes(value)

    with when:
        res = represent(sch)

    with then:
        assert res == expected_repr


def test_bytes_len_representation():
    with given:
        length = 10
        sch = schema.bytes.len(length)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes.len(10)"


def test_bytes_len_with_value_representation():
    with given:
        value = b"banana"
        length = 6
        sch = schema.bytes(value).len(length)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes(b'banana').len(6)"


def test_bytes_min_len_representation():
    with given:
        min_length = 1
        sch = schema.bytes.len(min_length, ...)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes.len(1, ...)"


def test_bytes_min_len_with_value_representation():
    with given:
        value = b"banana"
        min_length = 1
        sch = schema.bytes(value).len(min_length, ...)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes(b'banana').len(1, ...)"


def test_bytes_max_len_representation():
    with given:
        max_length = 10
        sch = schema.bytes.len(..., max_length)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes.len(..., 10)"


def test_bytes_max_len_with_value_representation():
    with given:
        value = b"banana"
        max_length = 10
        sch = schema.bytes(value).len(..., max_length)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes(b'banana').len(..., 10)"


def test_bytes_min_max_len_representation():
    with given:
        min_length = 1
        max_length = 10
        sch = schema.bytes.len(min_length, max_length)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes.len(1, 10)"


def test_bytes_min_max_len_with_value_representation():
    with given:
        value = b"banana"
        min_length = 1
        max_length = 10
        sch = schema.bytes(value).len(min_length, max_length)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.bytes(b'banana').len(1, 10)"
