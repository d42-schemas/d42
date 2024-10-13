import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_int_substitution():
    with given:
        sch = schema.int

    with when:
        res = substitute(sch, 42)

    with then:
        assert res == schema.int(42)
        assert res != sch


def test_int_value_substitution():
    with given:
        value = 42
        sch = schema.int(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.int(value)
        assert id(res) != id(sch)


def test_int_substitution_invalid_value_error():
    with given:
        sch = schema.int(42)

    with when, raises(Exception) as exception:
        substitute(sch, 3.14)

    with then:
        assert exception.type is SubstitutionError


def test_int_substitution_incorrect_value_error():
    with given:
        sch = schema.int(42)

    with when, raises(Exception) as exception:
        substitute(sch, 50)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [2, 1])
def test_int_substitution_min(value: int):
    with given:
        sch = schema.int.min(1)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.int(value).min(1)
        assert res != sch


def test_int_substitution_min_value_error():
    with given:
        sch = schema.int.min(1)

    with when, raises(Exception) as exception:
        substitute(sch, 0)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [0, 1])
def test_int_substitution_max(value: int):
    with given:
        sch = schema.int.max(1)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.int(value).max(1)
        assert res != sch


def test_int_substitution_max_value_error():
    with given:
        sch = schema.int.max(1)

    with when, raises(Exception) as exception:
        substitute(sch, 2)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [1, 2, 3])
def test_int_substitution_min_max(value: int):
    with given:
        sch = schema.int.min(1).max(3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.int(value).min(1).max(3)
        assert res != sch


@pytest.mark.parametrize("value", [0, 4])
def test_int_substitution_min_max_value_error(value: int):
    with given:
        sch = schema.int.min(1).max(3)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError
