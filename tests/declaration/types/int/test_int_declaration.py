from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import IntSchema


def test_int_declaration():
    with when:
        sch = schema.int

    with then:
        assert isinstance(sch, IntSchema)


def test_int_value_declaration():
    with given:
        value = 42

    with when:
        sch = schema.int(value)

    with then:
        assert sch.props.value == value


def test_int_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.int(3.14)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.int` value must be an instance of 'int', "
                                        "instance of 'float' 3.14 given")


def test_int_already_declared_declaration_error():
    with when, raises(Exception) as exception:
        schema.int(42)(42)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.int(42)` is already declared"


def test_int_min_value_declaration():
    with given:
        min_value = 1

    with when:
        sch = schema.int.min(min_value)

    with then:
        assert sch.props.min == min_value


def test_int_invalid_min_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.min(3.14)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.int` value must be an instance of 'int', "
                                        "instance of 'float' 3.14 given")


def test_int_value_already_declared_min_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.min(1)(42)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.int.min(1)` is already declared"


def test_int_min_value_already_declared_less_value_declaration_error():
    with given:
        sch = schema.int(42)

    with when, raises(Exception) as exception:
        sch.min(43)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min value must be less than or equal to 42, 43 given"
        )


def test_int_min_value_already_declared_min_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.min(1).min(2)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.int.min(1)` is already declared"


def test_int_max_value_declaration():
    with given:
        max_value = 2

    with when:
        sch = schema.int.max(max_value)

    with then:
        assert sch.props.max == max_value


def test_int_invalid_max_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.max(3.14)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.int` value must be an instance of 'int', "
                                        "instance of 'float' 3.14 given")


def test_int_value_already_declared_max_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.max(100)(42)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.int.max(100)` is already declared"


def test_int_max_value_already_declared_greater_value_declaration_error():
    with given:
        sch = schema.int(42)

    with when, raises(Exception) as exception:
        sch.max(41)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` max value must be greater than or equal to 42, 41 given"
        )


def test_int_max_value_already_declared_max_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.max(2).max(1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.int.max(2)` is already declared"


def test_int_min_max_value_declaration():
    with given:
        min_value, max_value = 1, 2

    with when:
        sch = schema.int.min(min_value).max(max_value)

    with then:
        assert sch.props.min == min_value
        assert sch.props.max == max_value


def test_int_min_max_with_value_declaration():
    with given:
        value = 2
        min_value, max_value = 1, 3

    with when:
        sch = schema.int(value).min(min_value).max(max_value)

    with then:
        assert sch.props.value == value
        assert sch.props.min == min_value
        assert sch.props.max == max_value


def test_int_multiple_of_declaration():
    with given:
        multiple_of_value = 3

    with when:
        sch = schema.int.multiple_of(multiple_of_value)

    with then:
        assert sch.props.multiple_of == multiple_of_value


def test_int_invalid_multiple_of_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.multiple_of(3.14)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.int` value must be an instance of 'int', "
                                        "instance of 'float' 3.14 given")


def test_int_multiple_of_value_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.multiple_of(0)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.int` multiple_of value must be greater than 0, 0 given"
        )


def test_int_value_already_declared_multiple_of_declaration_error():
    with when, raises(Exception) as exception:
        schema.int.multiple_of(2).multiple_of(42)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.int.multiple_of(2)` is already declared"


def test_int_multiple_of_value_applied():
    with given:
        value = 6
        multiple_of_value = 3

    with when:
        sch = schema.int(value).multiple_of(multiple_of_value)

    with then:
        assert sch.props.value == value
        assert sch.props.multiple_of == multiple_of_value
