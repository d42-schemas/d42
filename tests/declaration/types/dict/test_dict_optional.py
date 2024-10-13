from baby_steps import given, then, when
from pytest import raises

from d42 import optional


def test_optional():
    with given:
        key = "<key>"
        opt = optional(key)

    with when:
        res = opt.key

    with then:
        assert res == key


def test_optional_error():
    with when, raises(Exception) as exception:
        optional(...)

    with then:
        assert exception.type is TypeError


def test_optional_repr():
    with given:
        opt = optional("<key>")

    with when:
        res = repr(opt)

    with then:
        assert res == "optional('<key>')"


def test_optional_eq():
    with given:
        opt = optional("<key>")

    with when:
        res = opt == optional("<key>")

    with then:
        assert res is True


def test_optional_not_eq():
    with given:
        opt = optional("<key>")

    with when:
        res = opt == optional("<another key>")

    with then:
        assert res is False
