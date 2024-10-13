from typing import Any, List
from unittest.mock import sentinel

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema, substitute
from d42.substitution.errors import SubstitutionError


def test_list_of_no_elements_substitution():
    with given:
        sch = schema.list(schema.int)

    with when:
        res = substitute(sch, [])

    with then:
        assert res == schema.list([])
        assert res != sch


def test_list_of_elements_substitution():
    with given:
        sch = schema.list(schema.int)

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)])
        assert res != sch


def test_list_of_elements_substitution_error():
    with given:
        sch = schema.list

    with when, raises(Exception) as exception:
        substitute(sch, [sentinel])

    with then:
        assert exception.type is SubstitutionError


def test_list_of_substitution_invalid_value_error():
    with given:
        sch = schema.list(schema.int)

    with when, raises(Exception) as exception:
        substitute(sch, {})

    with then:
        assert exception.type is SubstitutionError


def test_list_of_substitution_incorrect_value_error():
    with given:
        sch = schema.list(schema.int)

    with when, raises(Exception) as exception:
        substitute(sch, ["1", "2"])

    with then:
        assert exception.type is SubstitutionError


def test_list_of_ellipsis_substitution_error():
    with given:
        sch = schema.list(schema.int)

    with when, raises(Exception) as exception:
        substitute(sch, [...])

    with then:
        assert exception.type is SubstitutionError


def test_list_of_all_ellipsis_substitution_error():
    with given:
        sch = schema.list(schema.int)

    with when, raises(Exception) as exception:
        substitute(sch, [..., ...])

    with then:
        assert exception.type is SubstitutionError


def test_list_of_substitution_head():
    with given:
        sch = schema.list(schema.int)

    with when:
        res = substitute(sch, [1, 2, ...])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2), ...])
        assert res != sch


def test_list_of_substitution_tail():
    with given:
        sch = schema.list(schema.int)

    with when:
        res = substitute(sch, [..., 1, 2])

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(2)])
        assert res != sch


def test_list_of_substitution_body():
    with given:
        sch = schema.list(schema.int)

    with when:
        res = substitute(sch, [..., 1, 2, ...])

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(2), ...])
        assert res != sch


def test_list_of_substitution_some_body_error():
    with given:
        sch = schema.list(schema.int)

    with when, raises(Exception) as exception:
        substitute(sch, [...])

    with then:
        assert exception.type is SubstitutionError


def test_list_of_len_substitution():
    with given:
        sch = schema.list(schema.int).len(2)

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)]).len(2)
        assert res != sch


@pytest.mark.parametrize("value", [
    [1],
    [1, 2, 3],
])
def test_list_of_len_substitution_error(value: List[Any]):
    with given:
        sch = schema.list(schema.int).len(2)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
])
def test_list_of_min_len_substitution(value: List[Any]):
    with given:
        sch = schema.list(schema.int).len(2, ...)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value]).len(2, ...)
        assert res != sch


def test_list_of_min_len_substitution_error():
    with given:
        sch = schema.list(schema.int).len(2, ...)

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
])
def test_list_of_max_len_substitution(value: List[Any]):
    with given:
        sch = schema.list(schema.int).len(..., 2)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value]).len(..., 2)
        assert res != sch


def test_list_of_max_len_substitution_error():
    with given:
        sch = schema.list(schema.int).len(..., 2)

    with when, raises(Exception) as exception:
        substitute(sch, [1, 2, 3])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1],
    [1, 2],
    [1, 2, 3],
])
def test_list_of_min_max_len_substitution(value: List[Any]):
    with given:
        sch = schema.list(schema.int).len(1, 3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value]).len(1, 3)
        assert res != sch


@pytest.mark.parametrize("value", [
    [],
    [1, 2, 3, 4],
])
def test_list_of_min_max_len_substitution_error(value: List[Any]):
    with given:
        sch = schema.list(schema.int).len(1, 3)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError
