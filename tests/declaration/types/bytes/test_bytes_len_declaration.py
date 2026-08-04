import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError


def test_bytes_len_declaration():
    with given:
        length = 10

    with when:
        sch = schema.bytes.len(length)

    with then:
        assert sch.props.len == length


def test_bytes_len_with_value_declaration():
    with given:
        value = b"banana"
        length = 6

    with when:
        sch = schema.bytes(value).len(length)

    with then:
        assert sch.props.value == value
        assert sch.props.len == length


def test_bytes_len_with_value_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes(b"banana").len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes(b'banana')` len must be equal to 6, 7 given"
        )


def test_bytes_invalid_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes` value must be an instance of 'int', "
            "instance of 'NoneType' None given"
        )


def test_bytes_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(7)` is already declared"


def test_bytes_len_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(1, ...).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(1, ...)` is already declared"


def test_bytes_len_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(..., 7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(..., 7)` is already declared"


def test_bytes_len_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(1, 7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(1, 7)` is already declared"


def test_bytes_value_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(7, ...)(b"banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(7, ...)` is already declared"


def test_bytes_value_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(7)(b"banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(7)` is already declared"


def test_bytes_min_len_declaration():
    with given:
        min_length = 10

    with when:
        sch = schema.bytes.len(min_length, ...)

    with then:
        assert sch.props.min_len == min_length


@pytest.mark.parametrize("min_length", [6, 5])
def test_bytes_min_len_with_value_declaration(min_length: int):
    with given:
        value = b"banana"

    with when:
        sch = schema.bytes(value).len(min_length, ...)

    with then:
        assert sch.props.value == value
        assert sch.props.min_len == min_length


def test_bytes_min_len_with_value_declaration_error():
    with given:
        value = b"banana"
        min_length = 7

    with when, raises(Exception) as exception:
        schema.bytes(value).len(min_length, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes(b'banana')` min len must be less than or "
            "equal to 6, 7 given"
        )


def test_bytes_invalid_min_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(None, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes` value must be an instance of 'int', "
            "instance of 'NoneType' None given"
        )


def test_bytes_min_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(7).len(1, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(7)` is already declared"


def test_bytes_max_len_declaration():
    with given:
        max_length = 10

    with when:
        sch = schema.bytes.len(..., max_length)

    with then:
        assert sch.props.max_len == max_length


@pytest.mark.parametrize("max_length", [6, 7])
def test_bytes_max_len_with_value_declaration(max_length: int):
    with given:
        value = b"banana"

    with when:
        sch = schema.bytes(value).len(..., max_length)

    with then:
        assert sch.props.value == value
        assert sch.props.max_len == max_length


def test_bytes_max_len_with_value_declaration_error():
    with given:
        value = b"banana"
        max_length = 5

    with when, raises(Exception) as exception:
        schema.bytes(value).len(..., max_length)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes(b'banana')` max len must be greater than or "
            "equal to 6, 5 given"
        )


def test_bytes_invalid_max_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(..., None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes` value must be an instance of 'int', "
            "instance of 'NoneType' None given"
        )


def test_bytes_max_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(7).len(..., 7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(7)` is already declared"


def test_bytes_value_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(..., 7)(b"banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(..., 7)` is already declared"


def test_bytes_min_max_len_declaration():
    with given:
        min_length, max_length = 1, 10

    with when:
        sch = schema.bytes.len(min_length, max_length)

    with then:
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


def test_bytes_invalid_min_length_type_with_max_length_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(None, 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes` value must be an instance of 'int', "
            "instance of 'NoneType' None given"
        )


def test_bytes_invalid_max_length_type_with_min_length_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(1, None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.bytes` value must be an instance of 'int', "
            "instance of 'NoneType' None given"
        )


def test_bytes_min_max_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(7).len(1, 7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(7)` is already declared"


def test_bytes_value_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.bytes.len(1, 7)(b"banana!")

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.bytes.len(1, 7)` is already declared"
