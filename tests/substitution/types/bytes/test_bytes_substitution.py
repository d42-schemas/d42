from baby_steps import given, then, when
from pytest import raises

from d42 import schema, substitute
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
