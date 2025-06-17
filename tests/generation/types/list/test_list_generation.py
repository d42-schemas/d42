from unittest.mock import call

import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.generation._consts import LIST_LEN_MAX, LIST_LEN_MIN

from ..._fixtures import *  # noqa: F401, F403
from ..._utils import schema_mock


def test_list_generation(*, generate, random_):
    with given:
        sch = schema.list

    with when:
        res = generate(sch)

    with then:
        assert res == []
        assert random_.mock_calls == [
            # this value is not actually used (implementation specific)
            call.random_int(LIST_LEN_MIN, LIST_LEN_MAX)
        ]


def test_list_no_elements_generation(*, generate, generator, random_):
    with given:
        sch = schema.list([])

    with when:
        res = generate(sch)

    with then:
        assert res == []
        assert random_.mock_calls == []


def test_list_elements_generation(*, generate, generator, random_):
    with given:
        val1, val2 = 1, 2
        elem1_ = schema_mock(return_value=val1)
        elem2_ = schema_mock(return_value=val2)
        sch = schema.list([elem1_, elem2_])

    with when:
        res = generate(sch)

    with then:
        assert res == [val1, val2]
        assert random_.mock_calls == []
        assert elem1_.mock_calls == [call.__accept__(generator)]
        assert elem2_.mock_calls == [call.__accept__(generator)]


def test_list_contains_no_elements_generation(*, generate, generator, random_):
    with given:
        sch = schema.list([...])

    with when:
        res = generate(sch)

    with then:
        assert res == []
        assert random_.mock_calls == []


def test_list_contains_head_elements_generation(*, generate, generator, random_):
    with given:
        val1, val2 = 1, 2
        elem1_ = schema_mock(return_value=val1)
        elem2_ = schema_mock(return_value=val2)
        sch = schema.list([elem1_, elem2_, ...])

    with when:
        res = generate(sch)

    with then:
        assert res == [val1, val2]
        assert random_.mock_calls == []
        assert elem1_.mock_calls == [call.__accept__(generator)]
        assert elem2_.mock_calls == [call.__accept__(generator)]


def test_list_contains_tail_elements_generation(*, generate, generator, random_):
    with given:
        val1, val2 = 1, 2
        elem1_ = schema_mock(return_value=val1)
        elem2_ = schema_mock(return_value=val2)
        sch = schema.list([..., elem1_, elem2_])

    with when:
        res = generate(sch)

    with then:
        assert res == [val1, val2]
        assert random_.mock_calls == []
        assert elem1_.mock_calls == [call.__accept__(generator)]
        assert elem2_.mock_calls == [call.__accept__(generator)]


def test_list_contains_elements_generation(*, generate, generator, random_):
    with given:
        val1, val2 = 1, 2
        elem1_ = schema_mock(return_value=val1)
        elem2_ = schema_mock(return_value=val2)
        sch = schema.list([..., elem1_, elem2_, ...])

    with when:
        res = generate(sch)

    with then:
        assert res == [val1, val2]
        assert random_.mock_calls == []
        assert elem1_.mock_calls == [call.__accept__(generator)]
        assert elem2_.mock_calls == [call.__accept__(generator)]


def test_list_len_generation(*, generate, random_):
    with given:
        list_len = 10
        sch = schema.list.len(list_len)

    with when:
        res = generate(sch)

    with then:
        assert res == [[]] * list_len
        assert random_.mock_calls == []


def test_list_min_len_generation(*, generate, random_):
    with given:
        list_min_len = 1
        sch = schema.list.len(list_min_len, ...)

        list_len = 5
        random_.random_int.return_value = list_len

    with when:
        res = generate(sch)

    with then:
        assert res == [[]] * list_len
        assert random_.mock_calls == [call.random_int(list_min_len, LIST_LEN_MAX)]


def test_list_max_len_generation(*, generate, random_):
    with given:
        list_max_len = 10
        sch = schema.list.len(..., list_max_len)

        list_len = 5
        random_.random_int.return_value = list_len

    with when:
        res = generate(sch)

    with then:
        assert res == [[]] * list_len
        assert random_.mock_calls == [call.random_int(LIST_LEN_MIN, list_max_len)]


def test_list_min_max_len_generation(*, generate, random_):
    with given:
        list_min_len, list_max_len = 1, 10
        sch = schema.list.len(list_min_len, list_max_len)

        list_len = 5
        random_.random_int.return_value = list_len

    with when:
        res = generate(sch)

    with then:
        assert res == [[]] * list_len
        assert random_.mock_calls == [call.random_int(list_min_len, list_max_len)]


def test_list_of_elements_generation(*, generate, generator, random_):
    with given:
        val = 42
        type_ = schema_mock(return_value=val)
        sch = schema.list(type_)

        list_len = 5
        random_.random_int.return_value = list_len

    with when:
        res = generate(sch)

    with then:
        assert res == [val] * list_len
        assert random_.mock_calls == [call.random_int(LIST_LEN_MIN, LIST_LEN_MAX)]
        assert type_.mock_calls == [call.__accept__(generator)] * list_len


def test_list_of_elements_len_generation(*, generate, generator, random_):
    with given:
        val = 42
        type_ = schema_mock(return_value=val)
        list_len = 10
        sch = schema.list(type_).len(list_len)

    with when:
        res = generate(sch)

    with then:
        assert res == [val] * list_len
        assert random_.mock_calls == []
        assert type_.mock_calls == [call.__accept__(generator)] * list_len


def test_list_of_elements_min_max_len_generation(*, generate, generator, random_):
    with given:
        val = 42
        type_ = schema_mock(return_value=val)
        list_min_len, list_max_len = 1, 10
        sch = schema.list(type_).len(list_min_len, list_max_len)

        list_len = 5
        random_.random_int.return_value = list_len

    with when:
        res = generate(sch)

    with then:
        assert res == [val] * list_len
        assert random_.mock_calls == [call.random_int(list_min_len, list_max_len)]
        assert type_.mock_calls == [call.__accept__(generator)] * list_len


def test_list_min_length_exceeding_max_limit(*, generate, random_):
    with given:
        list_min_len = LIST_LEN_MAX + 1
        sch = schema.list.len(list_min_len, ...)

    with when:
        res = generate(sch)

    with then:
        assert res == [[]] * list_min_len
        assert random_.mock_calls == [call.random_int(list_min_len, list_min_len)]


@pytest.mark.skipif(LIST_LEN_MIN < 1, reason="Test only applicable when LIST_LEN_MIN >= 1")
def test_list_max_length_below_min_limit(*, generate, random_):
    with given:
        list_max_len = LIST_LEN_MIN - 1
        sch = schema.list.len(..., list_max_len)

    with when:
        res = generate(sch)

    with then:
        assert res == [[]] * list_max_len
        assert random_.mock_calls == [call.random_int(list_max_len, list_max_len)]
