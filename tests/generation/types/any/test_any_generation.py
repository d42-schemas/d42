from unittest.mock import Mock, call

from baby_steps import given, then, when

from d42 import schema

from ..._fixtures import *  # noqa: F401, F403
from ..._utils import schema_mock


def test_any_generation(*, generate, random_):
    with given:
        sch = schema.any

    with when:
        res = generate(sch)

    with then:
        assert res is None
        assert random_.mock_calls == []


def test_any_type_generation(*, generate, generator, random_):
    with given:
        val = 42
        type_ = schema_mock(return_value=val)
        sch = schema.any(type_)

    with when:
        res = generate(sch)

    with then:
        assert res == val
        assert random_.mock_calls == [
            call.random_choice((type_,))
        ]
        assert type_.mock_calls == [call.__accept__(generator)]


def test_any_types_generation(*, generate, generator, random_):
    with given:
        val1, val2 = 42, "banana"
        type1_ = schema_mock(return_value=val1)
        type2_ = schema_mock(return_value=val2)
        sch = schema.any(type1_, type2_)
        random_.random_choice = Mock(return_value=type1_)

    with when:
        res = generate(sch)

    with then:
        assert res == val1
        assert random_.mock_calls == [
            call.random_choice((type1_, type2_))
        ]
        assert type1_.mock_calls == [call.__accept__(generator)]
