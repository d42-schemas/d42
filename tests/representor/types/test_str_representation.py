import pytest
from baby_steps import given, then, when

from d42 import schema
from d42.representation import represent


def test_str_representation():
    with given:
        sch = schema.str

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str"


@pytest.mark.parametrize(
    ("value", "expected_repr"),
    [
        ("", "schema.str('')"),
        (" ", "schema.str(' ')"),
        ("banana", "schema.str('banana')"),
    ]
)
def test_str_value_representation(value: str, expected_repr: str):
    with given:
        sch = schema.str(value)

    with when:
        res = represent(sch)

    with then:
        assert res == expected_repr


def test_str_len_representation():
    with given:
        sch = schema.str.len(10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.len(10)"


def test_str_min_len_representation():
    with given:
        sch = schema.str.len(1, ...)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.len(1, ...)"


def test_str_max_len_representation():
    with given:
        sch = schema.str.len(..., 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.len(..., 10)"


def test_str_min_max_len_representation():
    with given:
        sch = schema.str.len(1, 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.len(1, 10)"


def test_str_min_max_len_with_value_representation():
    with given:
        sch = schema.str("banana").len(1, 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str('banana').len(1, 10)"


def test_str_alphabet_representation():
    with given:
        sch = schema.str.alphabet("1234567890")

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.alphabet('1234567890')"


def test_str_alphabet_with_value_representation():
    with given:
        sch = schema.str("banana!").alphabet("abn!")

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str('banana!').alphabet('abn!')"


def test_str_contains_representation():
    with given:
        sch = schema.str.contains("banana")

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.contains('banana')"


def test_str_contains_with_value_representation():
    with given:
        sch = schema.str("banana").contains("banana")

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str('banana').contains('banana')"


def test_str_regex_representation():
    with given:
        sch = schema.str.regex(".*")

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str.regex('.*')"


def test_str_regex_with_value_representation():
    with given:
        sch = schema.str("banana").regex(".*")

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.str('banana').regex('.*')"
