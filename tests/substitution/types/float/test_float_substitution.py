import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_float_substitution():
    with given:
        sch = schema.float

    with when:
        res = substitute(sch, 3.14)

    with then:
        assert res == schema.float(3.14)
        assert res != sch


def test_float_value_substitution():
    with given:
        value = 3.14
        sch = schema.float(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.float(value)
        assert id(res) != id(sch)


def test_float_substitution_invalid_value_error():
    with given:
        sch = schema.float(3.14)

    with when, raises(Exception) as exception:
        substitute(sch, 42)

    with then:
        assert exception.type is SubstitutionError


def test_float_substitution_incorrect_value_error():
    with given:
        sch = schema.float(3.14)

    with when, raises(Exception) as exception:
        substitute(sch, 3.15)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [3.15, 3.14])
def test_float_substitution_min(value: int):
    with given:
        sch = schema.float.min(3.14)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.float(value).min(3.14)
        assert res != sch


def test_float_substitution_min_value_error():
    with given:
        sch = schema.float.min(3.14)

    with when, raises(Exception) as exception:
        substitute(sch, 3.13)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [3.14, 3.13])
def test_float_substitution_max(value: int):
    with given:
        sch = schema.float.max(3.14)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.float(value).max(3.14)
        assert res != sch


def test_float_substitution_max_value_error():
    with given:
        sch = schema.float.max(3.14)

    with when, raises(Exception) as exception:
        substitute(sch, 3.15)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [3.13, 3.14, 3.15])
def test_float_substitution_min_max(value: int):
    with given:
        sch = schema.float.min(3.13).max(3.15)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.float(value).min(3.13).max(3.15)
        assert res != sch


@pytest.mark.parametrize("value", [3.12, 3.16])
def test_float_substitution_min_max_value_error(value: int):
    with given:
        sch = schema.float.min(3.13).max(3.15)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError
