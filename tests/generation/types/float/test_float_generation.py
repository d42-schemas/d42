from unittest.mock import call

from baby_steps import given, then, when

from d42 import schema
from d42.generation._consts import FLOAT_MAX, FLOAT_MIN

from ..._fixtures import *  # noqa: F401, F403


def test_float_generation(*, generate, random_):
    with given:
        sch = schema.float

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, float)
        assert FLOAT_MIN <= res <= FLOAT_MAX
        assert random_.mock_calls == [
            call.random_float(FLOAT_MIN, FLOAT_MAX)
        ]


def test_float_value_generation(*, generate, random_):
    with given:
        val = 3.14
        sch = schema.float(val)

    with when:
        res = generate(sch)

    with then:
        assert res == val
        assert random_.mock_calls == []


def test_float_min_generation(*, generate, random_):
    with given:
        min_val = 3.14
        sch = schema.float.min(min_val)

    with when:
        res = generate(sch)

    with then:
        assert res >= min_val
        assert random_.mock_calls == [
            call.random_float(min_val, FLOAT_MAX)
        ]


def test_float_max_generation(*, generate, random_):
    with given:
        max_val = 6.28
        sch = schema.float.max(max_val)

    with when:
        res = generate(sch)

    with then:
        assert res <= max_val
        assert random_.mock_calls == [
            call.random_float(FLOAT_MIN, max_val)
        ]


def test_float_min_max_generation(*, generate, random_):
    with given:
        min_val, max_val = 3.14, 6.28
        sch = schema.float.min(min_val).max(max_val)

    with when:
        res = generate(sch)

    with then:
        assert min_val <= res <= max_val
        assert random_.mock_calls == [
            call.random_float(min_val, max_val)
        ]


def test_float_min_precision_generation(*, generate, random_):
    with given:
        min_val = 3.14
        precision = 5
        sch = schema.float.min(min_val).precision(precision)

    with when:
        res = generate(sch)

    with then:
        assert res >= min_val
        assert random_.mock_calls == [
            call.random_float(min_val, FLOAT_MAX, precision)
        ]


def test_float_max_precision_generation(*, generate, random_):
    with given:
        max_val = 6.28
        precision = 5
        sch = schema.float.max(max_val).precision(precision)

    with when:
        res = generate(sch)

    with then:
        assert res <= max_val
        assert random_.mock_calls == [
            call.random_float(FLOAT_MIN, max_val, precision)
        ]


def test_float_min_max_precision_generation(*, generate, random_):
    with given:
        min_val, max_val = 3.14, 6.28
        precision = 5
        sch = schema.float.min(min_val).max(max_val).precision(precision)

    with when:
        res = generate(sch)

    with then:
        assert min_val <= res <= max_val
        assert random_.mock_calls == [
            call.random_float(min_val, max_val, precision)
        ]


def test_float_precision_generation(*, generate, random_):
    with given:
        precision = 5
        sch = schema.float.precision(precision)

    with when:
        res = generate(sch)

    with then:
        assert FLOAT_MIN <= res <= FLOAT_MAX
        assert random_.mock_calls == [
            call.random_float(FLOAT_MIN, FLOAT_MAX, precision)
        ]
