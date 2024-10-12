import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError


def test_str_len_declaration():
    with given:
        length = 10

    with when:
        sch = schema.str.len(length)

    with then:
        assert sch.props.len == length


def test_str_len_with_value_declaration():
    with given:
        value = "banana"
        length = 6

    with when:
        sch = schema.str(value).len(length)

    with then:
        assert sch.props.value == value
        assert sch.props.len == length


def test_str_len_with_value_declaration_error():
    with when, raises(Exception) as exception:
        schema.str("banana").len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str('banana')` len must be equal to 6, 7 given"


def test_str_invalid_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_str_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(7)` is already declared"


def test_str_len_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(1, ...).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(1, ...)` is already declared"


def test_str_len_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(..., 7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(..., 7)` is already declared"


def test_str_len_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(1, 7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(1, 7)` is already declared"


def test_str_value_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(7, ...)("banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(7, ...)` is already declared"


def test_str_value_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(7)("banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(7)` is already declared"


def test_str_min_len_declaration():
    with given:
        min_length = 10

    with when:
        sch = schema.str.len(min_length, ...)

    with then:
        assert sch.props.min_len == min_length


@pytest.mark.parametrize("min_length", [6, 5])
def test_str_min_len_with_value_declaration(min_length):
    with given:
        value = "banana"

    with when:
        sch = schema.str(value).len(min_length, ...)

    with then:
        assert sch.props.value == value
        assert sch.props.min_len == min_length


def test_str_min_len_with_value_declaration_error():
    with given:
        value = "banana"
        min_length = 7

    with when, raises(Exception) as exception:
        schema.str(value).len(min_length, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str('banana')` min len must be less than or "
                                        "equal to 6, 7 given")


def test_str_invalid_min_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(None, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_str_min_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(7).len(1, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(7)` is already declared"


def test_str_max_len_declaration():
    with given:
        max_length = 10

    with when:
        sch = schema.str.len(..., max_length)

    with then:
        assert sch.props.max_len == max_length


@pytest.mark.parametrize("max_length", [6, 7])
def test_str_max_len_with_value_declaration(max_length: int):
    with given:
        value = "banana"

    with when:
        sch = schema.str(value).len(..., max_length)

    with then:
        assert sch.props.value == value
        assert sch.props.max_len == max_length


def test_str_max_len_with_value_declaration_error():
    with given:
        value = "banana"
        max_length = 5

    with when, raises(Exception) as exception:
        schema.str(value).len(..., max_length)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str('banana')` max len must be greater than or "
                                        "equal to 6, 5 given")


def test_str_invalid_max_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(..., None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_str_max_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(7).len(..., 7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(7)` is already declared"


def test_str_value_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(..., 7)("banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(..., 7)` is already declared"


def test_str_min_max_len_declaration():
    with given:
        min_length, max_length = 1, 10

    with when:
        sch = schema.str.len(min_length, max_length)

    with then:
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


def test_str_invalid_min_length_type_with_max_length_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(None, 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_str_invalid_max_length_type_with_min_length_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(1, None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.str` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_str_min_max_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(7).len(1, 7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(7)` is already declared"


def test_str_value_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.str.len(1, 7)("banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.str.len(1, 7)` is already declared"
