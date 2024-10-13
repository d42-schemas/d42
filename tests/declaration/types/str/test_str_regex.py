import string

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import StrSchema


def test_str_regex_declaration():
    with given:
        pattern = ".*"

    with when:
        sch = schema.str.regex(pattern)

    with then:
        assert isinstance(sch, StrSchema)
        assert sch.props.pattern == pattern


def test_str_invalid_regex_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.regex(42)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'str', "
                                        "instance of 'int' 42 given")


def test_str_invalid_regex_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.regex("*")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "Invalid pattern (nothing to repeat at position 0)"


@pytest.mark.parametrize("pattern", [".*", "banana"])
def test_str_pattern_with_value_declaration(pattern: str):

    with when:
        sch = schema.str("banana").regex(pattern)

    with then:
        assert sch.props.pattern == pattern


def test_str_pattern_already_declared_value_declaration_error():
    with given:
        sch = schema.str("banana")
        pattern = "[0-9]+"

    with when, raises(Exception) as exception:
        sch.regex(pattern)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`{sch!r}` does not match {pattern!r}"


@pytest.mark.parametrize("declare", [
    lambda sch: sch.regex(".*"),
    lambda sch: sch("banana"),
    lambda sch: sch.len(1),
    lambda sch: sch.alphabet(string.ascii_letters),
    lambda sch: sch.contains("banana"),
])
def test_str_already_declared_regex_declaration_error(declare):
    with given:
        sch = schema.str.regex(".*")

    with when, raises(Exception) as exception:
        declare(sch)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.regex('.*')` is already declared"
