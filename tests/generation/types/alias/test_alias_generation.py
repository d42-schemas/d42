from unittest.mock import call

from baby_steps import given, then, when

from d42 import schema
from d42.declaration.types import TypeAliasSchema
from d42.generation._consts import INT_MAX

from ..._fixtures import *  # noqa: F401, F403
from ..._utils import schema_mock


def test_alias_default_generation(*, generate, random_):
    with given:
        sch = TypeAliasSchema()

    with when:
        res = generate(sch)

    with then:
        assert res is None
        assert random_.mock_calls == []


def test_alias_type_generation(*, generate, generator, random_):
    with given:
        val = 42
        type_ = schema_mock(return_value=val)
        sch = schema.alias("custom_schema", schema.any(type_))

    with when:
        res = generate(sch)

    with then:
        assert res == val
        assert random_.mock_calls == [
            call.random_choice((type_,))
        ]
        assert type_.mock_calls == [call.__accept__(generator)]


def test_alias_generation(*, generate, random_):
    with given:
        min_val = 0
        sch = schema.alias("uint_schema", schema.int.min(min_val))

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, int)
        assert min_val <= res <= INT_MAX
        assert random_.mock_calls == [
            call.random_int(min_val, INT_MAX)
        ]
