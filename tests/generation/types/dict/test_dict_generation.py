from unittest.mock import call

from baby_steps import given, then, when

from d42 import optional, schema

from ..._fixtures import *  # noqa: F401, F403
from ..._utils import schema_mock


def test_dict_generation(*, generate, random_):
    with given:
        sch = schema.dict

    with when:
        res = generate(sch)

    with then:
        assert res == {}


def test_dict_empty_keys_generation(*, generate, random_):
    with given:
        sch = schema.dict({})

    with when:
        res = generate(sch)

    with then:
        assert res == {}


def test_dict_keys_generation(*, generate, generator, random_):
    with given:
        type1_ = schema_mock(return_value=42)
        type2_ = schema_mock(return_value="banana")
        sch = schema.dict({
            "id": type1_,
            "name": type2_,
        })

    with when:
        res = generate(sch)

    with then:
        assert res == {
            "id": 42,
            "name": "banana",
        }
        assert random_.mock_calls == []
        assert type1_.mock_calls == [call.__accept__(generator)]
        assert type2_.mock_calls == [call.__accept__(generator)]


def test_dict_relaxed_empty_keys_generation(*, generate, random_):
    with given:
        sch = schema.dict({...: ...})

    with when:
        res = generate(sch)

    with then:
        assert res == {}


def test_dict_relaxed_keys_generation(*, generate, generator, random_):
    with given:
        type1_ = schema_mock(return_value=42)
        type2_ = schema_mock(return_value="banana")
        sch = schema.dict({
            "id": type1_,
            "name": type2_,
            ...: ...
        })

    with when:
        res = generate(sch)

    with then:
        assert res == {
            "id": 42,
            "name": "banana",
        }
        assert random_.mock_calls == []
        assert type1_.mock_calls == [call.__accept__(generator)]
        assert type2_.mock_calls == [call.__accept__(generator)]


def test_dict_with_optional_key_generation(*, generate, generator, random_):
    with given:
        type1_ = schema_mock(return_value=42)
        type2_ = schema_mock(return_value="banana")
        sch = schema.dict({
            "id": type1_,
            optional("name"): type2_,
        })

    with when:
        res = generate(sch)

    with then:
        assert res == {"id": 42}
        assert random_.mock_calls == []
        assert type1_.mock_calls == [call.__accept__(generator)]
        assert type2_.mock_calls == []
