from baby_steps import given, then, when

from d42 import schema

from ..._fixtures import *  # noqa: F401, F403


def test_none_generation(*, generate, random_):
    with given:
        sch = schema.none

    with when:
        res = generate(sch)

    with then:
        assert res is None
        assert random_.mock_calls == []
