from unittest.mock import call

from baby_steps import given, then, when

from d42 import schema
from d42.generation._consts import INT_MAX, INT_MIN

from ..._fixtures import *  # noqa: F401, F403


def test_int_generation(*, generate, random_):
    with given:
        sch = schema.int

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, int)
        assert INT_MIN <= res <= INT_MAX
        assert random_.mock_calls == [
            call.random_int(INT_MIN, INT_MAX)
        ]


def test_int_value_generation(*, generate, random_):
    with given:
        val = 42
        sch = schema.int(val)

    with when:
        res = generate(sch)

    with then:
        assert res == val
        assert random_.mock_calls == []


def test_int_min_generation(*, generate, random_):
    with given:
        min_val = 1
        sch = schema.int.min(min_val)

    with when:
        res = generate(sch)

    with then:
        assert res >= min_val
        assert random_.mock_calls == [
            call.random_int(min_val, INT_MAX)
        ]


def test_int_max_generation(*, generate, random_):
    with given:
        max_val = 2
        sch = schema.int.max(max_val)

    with when:
        res = generate(sch)

    with then:
        assert res <= max_val
        assert random_.mock_calls == [
            call.random_int(INT_MIN, max_val)
        ]


def test_int_min_max_generation(*, generate, random_):
    with given:
        min_val, max_val = 1, 2
        sch = schema.int.min(min_val).max(max_val)

    with when:
        res = generate(sch)

    with then:
        assert min_val <= res <= max_val
        assert random_.mock_calls == [
            call.random_int(min_val, max_val)
        ]
