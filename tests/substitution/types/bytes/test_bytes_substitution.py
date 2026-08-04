import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_bytes_substitution():
    with given:
        sch = schema.bytes

    with when:
        res = substitute(sch, b"banana")

    with then:
        assert res == schema.bytes(b"banana")
        assert res != sch


def test_bytes_value_substitution():
    with given:
        value = b"banana"
        sch = schema.bytes(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.bytes(value)
        assert id(res) != id(sch)


def test_bytes_substitution_invalid_value_error():
    with given:
        sch = schema.bytes(b"banana")

    with when, raises(Exception) as exception:
        substitute(sch, "banana")

    with then:
        assert exception.type is SubstitutionError


def test_bytes_substitution_incorrect_value_error():
    with given:
        sch = schema.bytes(b"banana")

    with when, raises(Exception) as exception:
        substitute(sch, b"cucumber")

    with then:
        assert exception.type is SubstitutionError


def test_bytes_substitution_len():
    with given:
        value = b"123"
        sch = schema.bytes.len(3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.bytes(value).len(3)
        assert res != sch


@pytest.mark.parametrize("value", [b"12", b"1234"])
def test_bytes_substitution_len_error(value: bytes):
    with given:
        sch = schema.bytes.len(3)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [b"123", b"1234"])
def test_bytes_substitution_min_len(value: bytes):
    with given:
        sch = schema.bytes.len(3, ...)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.bytes(value).len(3, ...)
        assert res != sch


def test_bytes_substitution_min_len_error():
    with given:
        sch = schema.bytes.len(3, ...)

    with when, raises(Exception) as exception:
        substitute(sch, b"12")

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [b"", b"12", b"123"])
def test_bytes_substitution_max_len(value: bytes):
    with given:
        sch = schema.bytes.len(..., 3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.bytes(value).len(..., 3)
        assert res != sch


def test_bytes_substitution_max_len_error():
    with given:
        sch = schema.bytes.len(..., 3)

    with when, raises(Exception) as exception:
        substitute(sch, b"1234")

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [b"12", b"123", b"1234"])
def test_bytes_substitution_min_max_len(value: bytes):
    with given:
        sch = schema.bytes.len(2, 4)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.bytes(value).len(2, 4)
        assert res != sch


@pytest.mark.parametrize("value", [b"1", b"12345"])
def test_bytes_substitution_min_max_len_error(value: bytes):
    with given:
        sch = schema.bytes.len(2, 4)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError
