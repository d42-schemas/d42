import string
from unittest.mock import Mock, call

import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.generation._consts import STR_ALPHABET, STR_LEN_MAX, STR_LEN_MIN

from ..._fixtures import *  # noqa: F401, F403


def test_str_generation(*, generate, random_):
    with given:
        sch = schema.str

        str_len = 25
        random_.random_int.return_value = str_len

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, str)
        assert STR_LEN_MIN <= len(res) <= STR_LEN_MAX
        assert random_.mock_calls == [
            call.random_int(STR_LEN_MIN, STR_LEN_MAX),
            call.random_str(str_len, STR_ALPHABET)
        ]


def test_str_value_generation(*, generate, random_):
    with given:
        val = "banana"
        sch = schema.str(val)

    with when:
        res = generate(sch)

    with then:
        assert res == val
        assert random_.mock_calls == []


def test_str_len_generation(*, generate, random_):
    with given:
        str_len = 10
        sch = schema.str.len(str_len)

    with when:
        res = generate(sch)

    with then:
        assert len(res) == str_len
        assert random_.mock_calls == [
            call.random_str(str_len, STR_ALPHABET)
        ]


def test_str_min_len_generation(*, generate, random_):
    with given:
        str_min_len = 1
        sch = schema.str.len(str_min_len, ...)

        str_len = 5
        random_.random_int.return_value = str_len

    with when:
        res = generate(sch)

    with then:
        assert str_min_len <= len(res) <= STR_LEN_MAX
        assert random_.mock_calls == [
            call.random_int(str_min_len, STR_LEN_MAX),
            call.random_str(str_len, STR_ALPHABET)
        ]


def test_str_len_max_generation(*, generate, random_):
    with given:
        str_max_len = 10
        str_len = 5
        random_.random_int.return_value = str_len
        sch = schema.str.len(..., str_max_len)

    with when:
        res = generate(sch)

    with then:
        assert STR_LEN_MIN <= len(res) <= str_max_len
        assert random_.mock_calls == [
            call.random_int(STR_LEN_MIN, str_max_len),
            call.random_str(str_len, STR_ALPHABET)
        ]


def test_str_len_min_max_generation(*, generate, random_):
    with given:
        str_min_len, str_max_len = 1, 10
        sch = schema.str.len(str_min_len, str_max_len)

        str_len = 5
        random_.random_int.return_value = str_len

    with when:
        res = generate(sch)

    with then:
        assert str_min_len <= len(res) <= str_max_len
        assert random_.mock_calls == [
            call.random_int(str_min_len, str_max_len),
            call.random_str(str_len, STR_ALPHABET)
        ]


def test_str_alphabet_generation(*, generate, random_):
    with given:
        str_alphabet = string.digits
        sch = schema.str.alphabet(str_alphabet)

        str_len = 5
        random_.random_int.return_value = str_len

    with when:
        res = generate(sch)

    with then:
        assert STR_LEN_MIN <= len(res) <= STR_LEN_MAX
        assert random_.mock_calls == [
            call.random_int(STR_LEN_MIN, STR_LEN_MAX),
            call.random_str(str_len, str_alphabet)
        ]


def test_str_alphabet_len_generation(*, generate, random_):
    with given:
        str_len = 5
        str_alphabet = string.digits
        sch = schema.str.alphabet(str_alphabet).len(str_len)

    with when:
        res = generate(sch)

    with then:
        assert len(res) == str_len
        assert random_.mock_calls == [
            call.random_str(str_len, str_alphabet)
        ]


def test_str_alphabet_min_max_len_generation(*, generate, random_):
    with given:
        str_min_len, str_max_len = 1, 10
        str_alphabet = string.digits
        sch = schema.str.alphabet(str_alphabet).len(str_min_len, str_max_len)

        str_len = 5
        random_.random_int.return_value = str_len

    with when:
        res = generate(sch)

    with then:
        assert str_min_len <= len(res) <= str_max_len
        assert random_.mock_calls == [
            call.random_int(str_min_len, str_max_len),
            call.random_str(str_len, str_alphabet)
        ]


@pytest.mark.parametrize("substr", ["banana", " ", ""])
def test_str_contains_generation(substr: str, *, generate, random_):
    with given:
        sch = schema.str.contains(substr)

        str_len = 15
        random_.random_int.return_value = str_len

    with when:
        res = generate(sch)

    with then:
        assert substr in res
        assert random_.mock_calls == [
            call.random_int(len(substr), STR_LEN_MAX),
            call.random_str(str_len - len(substr), STR_ALPHABET),
            call.random_int(0, str_len - len(substr)),
        ]


@pytest.mark.parametrize("length", [5, 6, 7])
def test_str_contains_with_len_generation(length: int, *, generate):
    with given:
        substr = "banana"
        sch = schema.str.contains(substr).len(length)

    with when:
        res = generate(sch)

    with then:
        assert substr in res
        assert len(res) == max(length, len(substr))


@pytest.mark.parametrize("min_length", [5, 6, 7])
def test_str_contains_with_min_len_generation(min_length: int, *, generate, random_):
    with given:
        substr = "banana"
        substr_len = max(len(substr), min_length)
        sch = schema.str.contains(substr).len(min_length, ...)

        str_len = 15
        random_.random_int = Mock(side_effect=(str_len, 0))

    with when:
        res = generate(sch)

    with then:
        assert res.startswith(substr)
        assert random_.mock_calls == [
            call.random_int(substr_len, STR_LEN_MAX),
            call.random_str(str_len - len(substr), STR_ALPHABET),
            call.random_int(0, str_len - len(substr)),
        ]


@pytest.mark.parametrize("max_length", [5, 6, 7])
def test_str_contains_with_max_len_generation(max_length: int, *, generate, random_):
    with given:
        substr = "banana"
        substr_len = max(len(substr), max_length)
        sch = schema.str.contains(substr).len(..., max_length)

        str_len = 15
        random_.random_int = Mock(side_effect=(str_len, str_len - len(substr)))

    with when:
        res = generate(sch)

    with then:
        assert res.endswith(substr)
        assert random_.mock_calls == [
            call.random_int(len(substr), substr_len),
            call.random_str(str_len - len(substr), STR_ALPHABET),
            call.random_int(0, str_len - len(substr)),
        ]


def test_str_regex_generation(*, generate, random_):
    with when:
        res = generate(schema.str.regex(r"ab"))

    with then:
        assert res == "ab"
        assert random_.mock_calls == []


def test_str_regex_pattern_generation(*, generate, random_):
    with given:
        repeat = 2
        random_.random_int.return_value = repeat

    with when:
        res = generate(schema.str.regex(r"a+"))

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(1, 32)
        ]


def test_str_min_length_exceeding_max_limit(*, generate, random_):
    with given:
        str_min_len = STR_LEN_MAX + 1
        sch = schema.str.len(str_min_len, ...)

    with when:
        res = generate(sch)

    with then:
        assert len(res) == str_min_len
        assert random_.mock_calls == [
            call.random_int(str_min_len, str_min_len),
            call.random_str(str_min_len, STR_ALPHABET),
        ]


@pytest.mark.skipif(STR_LEN_MIN < 1, reason="Test only applicable when STR_LEN_MIN >= 1")
def test_str_max_length_below_min_limit(*, generate, random_):
    with given:
        str_max_len = STR_LEN_MIN - 1
        sch = schema.str.len(..., str_max_len)

    with when:
        res = generate(sch)

    with then:
        assert len(res) == str_max_len
        assert random_.mock_calls == [
            call.random_int(str_max_len, str_max_len),
            call.random_str(str_max_len, STR_ALPHABET),
        ]
