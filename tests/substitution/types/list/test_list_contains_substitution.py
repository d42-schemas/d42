from typing import Any, List

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.substitution import substitute
from d42.substitution.errors import SubstitutionError


def test_list_contains_empty_substitution():
    with given:
        sch = schema.list([...])

    with when:
        res = substitute(sch, [])

    with then:
        assert res == schema.list([])
        assert res != sch


def test_list_contains_elements_substitution():
    with given:
        sch = schema.list([...])

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)])
        assert res != sch


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
])
def test_list_contains_head_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_contains_head_less_elements_substitution_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1, 2],
    [0, 1, 2],
])
def test_list_contains_tail_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_contains_tail_less_elements_substitution_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1, 2],
    [0, 1, 2, 3],
    [0, 1, 2],
    [1, 2, 3],
])
def test_list_contains_body_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_contains_body_less_elements_substitution_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_body_empty_elements_substitution_error():
    with given:
        sch = schema.list([..., schema.int, ...])

    with when, raises(Exception) as exception:
        substitute(sch, [])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_body_elements_with_len_substitution():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...]).len(2)

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)]).len(2)
        assert res != sch


@pytest.mark.parametrize("value", [
    [1, 2, 3],
    [0, 1, 2],
    [0, 1, 2, 3],
])
def test_list_contains_body_elements_with_len_substitution_error(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...]).len(2)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_some_substitution_error():
    with given:
        sch = schema.list([...])

    with when, raises(Exception) as exception:
        substitute(sch, [...])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_ellipsis_substitution_error():
    with given:
        sch = schema.list

    with when, raises(Exception) as exception:
        substitute(sch, [...])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_all_ellipsis_substitution_error():
    with given:
        sch = schema.list

    with when, raises(Exception) as exception:
        substitute(sch, [..., ...])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_substitution_head():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, [1, 2, ...])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2), ...])
        assert res != sch


def test_list_contains_substitution_tail():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, [..., 1, 2])

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(2)])
        assert res != sch


def test_list_contains_substitution_body():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, [..., 1, 2, ...])

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(2), ...])
        assert res != sch
