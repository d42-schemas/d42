from unittest.mock import call

from baby_steps import given, then, when

from d42 import schema

from ..._fixtures import *  # noqa: F401, F403


def test_bool_generation(*, generate, random_):
    with given:
        sch = schema.bool

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, bool)
        assert random_.mock_calls == [
            call.random_choice((True, False))
        ]


def test_bool_value_generation(*, generate, random_):
    with given:
        sch = schema.bool(True)

    with when:
        res = generate(sch)

    with then:
        assert res is True
        assert random_.mock_calls == []
