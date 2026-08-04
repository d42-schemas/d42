from unittest.mock import call

from baby_steps import given, then, when

from d42 import schema
from d42.generation._consts import BYTES_LEN_MAX, BYTES_LEN_MIN, STR_ALPHABET

from ..._fixtures import *  # noqa: F401, F403


def test_bytes_generation(*, generate, random_):
    with given:
        sch = schema.bytes

        length = 25
        random_.random_int.return_value = length

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, bytes)
        assert BYTES_LEN_MIN <= len(res) <= BYTES_LEN_MAX
        assert random_.mock_calls == [
            call.random_int(BYTES_LEN_MIN, BYTES_LEN_MAX),
            call.random_str(length, STR_ALPHABET)
        ]


def test_bytes_value_generation(*, generate, random_):
    with given:
        val = b"banana"
        sch = schema.bytes(val)

    with when:
        res = generate(sch)

    with then:
        assert res == val
        assert random_.mock_calls == []


def test_bytes_len_generation(*, generate, random_):
    with given:
        length = 10
        sch = schema.bytes.len(length)

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, bytes)
        assert len(res) == length
        assert random_.mock_calls == [
            call.random_str(length, STR_ALPHABET),
        ]


def test_bytes_min_len_generation(*, generate, random_):
    with given:
        min_length = 10
        length = 25
        sch = schema.bytes.len(min_length, ...)
        random_.random_int.return_value = length

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, bytes)
        assert len(res) == length
        assert random_.mock_calls == [
            call.random_int(min_length, BYTES_LEN_MAX),
            call.random_str(length, STR_ALPHABET),
        ]


def test_bytes_max_len_generation(*, generate, random_):
    with given:
        max_length = 30
        length = 25
        sch = schema.bytes.len(..., max_length)
        random_.random_int.return_value = length

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, bytes)
        assert len(res) == length
        assert random_.mock_calls == [
            call.random_int(BYTES_LEN_MIN, max_length),
            call.random_str(length, STR_ALPHABET),
        ]


def test_bytes_min_max_len_generation(*, generate, random_):
    with given:
        min_length = 10
        max_length = 30
        length = 25
        sch = schema.bytes.len(min_length, max_length)
        random_.random_int.return_value = length

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, bytes)
        assert len(res) == length
        assert random_.mock_calls == [
            call.random_int(min_length, max_length),
            call.random_str(length, STR_ALPHABET),
        ]
