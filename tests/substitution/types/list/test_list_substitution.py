from typing import Any, List

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
])
def test_list_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_exact_elements_substitution():
    with given:
        sch = schema.list([schema.int, schema.int, schema.int])

    with when:
        res = substitute(sch, [1, 2, 3])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2), schema.int(3)])
        assert res != sch


def test_list_less_elements_substitution_error():
    with given:
        sch = schema.list([schema.int, schema.int, schema.int])

    with when, raises(Exception) as exception:
        substitute(sch, [1, 2])

    with then:
        assert exception.type is SubstitutionError


def test_list_more_elements_substitution_error():
    with given:
        sch = schema.list([schema.int, schema.int, schema.int])

    with when, raises(Exception) as exception:
        substitute(sch, [1, 2, 3, 4])

    with then:
        assert exception.type is SubstitutionError


def test_list_len_substitution():
    with given:
        sch = schema.list.len(2)

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)]).len(2)
        assert res != sch


@pytest.mark.parametrize("value", [
    [1],
    [1, 2, 3],
])
def test_list_len_substitution_error(value: List[Any]):
    with given:
        sch = schema.list.len(2)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
])
def test_list_min_len_substitution(value: Any):
    with given:
        sch = schema.list.len(2, ...)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value]).len(2, ...)
        assert res != sch


def test_list_min_len_substitution_error():
    with given:
        sch = schema.list.len(2, ...)

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
])
def test_list_max_len_substitution(value: List[Any]):
    with given:
        sch = schema.list.len(..., 2)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value]).len(..., 2)
        assert res != sch


def test_list_max_len_substitution_error():
    with given:
        sch = schema.list.len(..., 2)

    with when, raises(Exception) as exception:
        substitute(sch, [1, 2, 3])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1],
    [1, 2],
    [1, 2, 3],
])
def test_list_min_max_len_substitution(value: List[Any]):
    with given:
        sch = schema.list.len(1, 3)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value]).len(1, 3)
        assert res != sch


@pytest.mark.parametrize("value", [
    [],
    [1, 2, 3, 4],
])
def test_list_min_max_len_substitution_error(value: List[Any]):
    with given:
        sch = schema.list.len(1, 3)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError
