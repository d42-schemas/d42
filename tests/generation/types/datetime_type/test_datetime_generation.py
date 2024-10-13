from datetime import datetime

from baby_steps import given, then, when

from d42 import schema

from ..._fixtures import *  # noqa: F401, F403


def test_datetime_generation(*, generate, random_):
    with given:
        sch = schema.datetime

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, datetime)
        assert random_.mock_calls == []


def test_datetime_value_generation(*, generate, random_):
    with given:
        dt = datetime.now()
        sch = schema.datetime(dt)

    with when:
        res = generate(sch)

    with then:
        assert res == dt
        assert random_.mock_calls == []
