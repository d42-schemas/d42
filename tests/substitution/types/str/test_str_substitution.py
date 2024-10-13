import string

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_str_substitution():
    with given:
        sch = schema.str

    with when:
        res = substitute(sch, "banana")

    with then:
        assert res == schema.str("banana")
        assert res != sch


def test_str_value_substitution():
    with given:
        value = "banana"
        sch = schema.str(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value)
        assert id(res) != id(sch)


def test_str_substitution_invalid_value_error():
    with given:
        sch = schema.str("banana")

    with when, raises(Exception) as exception:
        substitute(sch, [])

    with then:
        assert exception.type is SubstitutionError


def test_str_substitution_incorrect_value_error():
    with given:
        sch = schema.str("banana")

    with when, raises(Exception) as exception:
        substitute(sch, "cucumber")

    with then:
        assert exception.type is SubstitutionError


def test_str_substitution_len():
    with given:
        value = "123"
        sch = schema.str.len(3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).len(3)
        assert res != sch


@pytest.mark.parametrize("value", ["12", "1234"])
def test_str_substitution_len_error(value: str):
    with given:
        sch = schema.str.len(3)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", ["123", "1234"])
def test_str_substitution_min_len(value: str):
    with given:
        sch = schema.str.len(3, ...)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).len(3, ...)
        assert res != sch


def test_str_substitution_min_len_error():
    with given:
        sch = schema.str.len(3, ...)

    with when, raises(Exception) as exception:
        substitute(sch, "12")

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", ["", "12", "123"])
def test_str_substitution_max_len(value: str):
    with given:
        sch = schema.str.len(..., 3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).len(..., 3)
        assert res != sch


def test_str_substitution_max_len_error():
    with given:
        sch = schema.str.len(..., 3)

    with when, raises(Exception) as exception:
        substitute(sch, "1234")

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", ["12", "123", "1234"])
def test_str_substitution_min_max_len(value: str):
    with given:
        sch = schema.str.len(2, 4)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).len(2, 4)
        assert res != sch


@pytest.mark.parametrize("value", ["1", "12345"])
def test_str_substitution_min_max_len_error(value: str):
    with given:
        sch = schema.str.len(2, 4)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", ["", "banana"])
def test_str_substitution_alphabet(value: str):
    with given:
        letters = string.ascii_letters
        sch = schema.str.alphabet(letters)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).alphabet(letters)
        assert res != sch


def test_str_substitution_alphabet_error():
    with given:
        letters = string.ascii_letters
        sch = schema.str.alphabet(letters)

    with when, raises(Exception) as exception:
        substitute(sch, "1234")

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("substr", ["", "anan", "banana"])
def test_str_substitution_substr(substr: str):
    with given:
        value = "banana"
        sch = schema.str.contains(substr)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).contains(substr)
        assert res != sch


@pytest.mark.parametrize("value", ["", "yellow"])
def test_str_substitution_substr_error(value: str):
    with given:
        sch = schema.str.contains("banana")

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


def test_str_substitution_regex():
    with given:
        pattern = "[a-z]+"
        sch = schema.str.regex(pattern)
        value = "banana"

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.str(value).regex(pattern)
        assert res != sch


def test_str_substitution_regex_error():
    with given:
        pattern = "[0-9]+"
        sch = schema.str.regex(pattern)
        value = "banana"

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError
