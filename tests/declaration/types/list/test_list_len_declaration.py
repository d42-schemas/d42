from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError


def test_list_len_declaration():
    with given:
        length = 10

    with when:
        sch = schema.list.len(length)

    with then:
        assert sch.props.len == length


def test_list_invalid_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.list` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_list_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(7)` is already declared"


def test_list_min_len_declaration():
    with given:
        min_length = 10

    with when:
        sch = schema.list.len(min_length, ...)

    with then:
        assert sch.props.min_len == min_length


def test_list_invalid_min_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(None, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.list` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_list_len_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, ...).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1, ...)` is already declared"


def test_list_min_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(7).len(1, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(7)` is already declared"


def test_list_max_len_declaration():
    with given:
        max_length = 10

    with when:
        sch = schema.list.len(..., max_length)

    with then:
        assert sch.props.max_len == max_length


def test_list_invalid_max_length_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(..., None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.list` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_list_invalid_max_length_type_with_min_length_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, None)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.list` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_list_len_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(..., 7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(..., 7)` is already declared"


def test_list_max_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(7).len(..., 7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(7)` is already declared"


def test_list_min_max_len_declaration():
    with given:
        min_length, max_length = 1, 10

    with when:
        sch = schema.list.len(min_length, max_length)

    with then:
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


def test_list_min_max_same_len_declaration():
    with given:
        min_length, max_length = 5, 5

    with when:
        sch = schema.list.len(min_length, max_length)

    with then:
        assert sch.props.min_len == min_length
        assert sch.props.max_len == max_length


def test_list_invalid_min_length_type_with_max_length_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(None, 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.list` value must be an instance of 'int', "
                                        "instance of 'NoneType' None given")


def test_list_len_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, 7).len(7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1, 7)` is already declared"


def test_list_min_max_len_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(7).len(1, 7)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(7)` is already declared"


def test_list_value_already_declared_min_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, 2)([schema.int(1)])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1, 2)` is already declared"


def test_list_with_elements_len_declaration():
    with given:
        length = 1

    with when:
        sch = schema.list([schema.int]).len(length)

    with then:
        assert sch.props.len == length


def test_list_value_already_declared_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1)([schema.int(1)])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1)` is already declared"


def test_list_with_elements_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`{sch!r}` len must be equal to 2, 1 given"


def test_list_with_elements_min_len_declaration():
    with given:
        length = 1

    with when:
        sch = schema.list([schema.int]).len(length, ...)

    with then:
        assert sch.props.min_len == length


def test_list_value_already_declared_min_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(1, ...)([schema.int(1)])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(1, ...)` is already declared"


def test_list_with_elements_min_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(3, ...)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` min len must be less than or equal to 2, 3 given"
        )


def test_list_with_elements_max_len_declaration():
    with given:
        length = 1

    with when:
        sch = schema.list([schema.int]).len(..., length)

    with then:
        assert sch.props.max_len == length


def test_list_value_already_declared_max_len_declaration_error():
    with when, raises(Exception) as exception:
        schema.list.len(..., 1)([schema.int(1)])

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.list.len(..., 1)` is already declared"


def test_list_with_elements_max_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(..., 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` max len must be greater than or equal to 2, 1 given"
        )


def test_list_with_elements_min_max_same_len_declaration():
    with given:
        length = 1

    with when:
        sch = schema.list([schema.int]).len(length, length)

    with then:
        assert sch.props.min_len == length
        assert sch.props.max_len == length


def test_list_with_elements_min_max_len_declaration_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        sch.len(2, 1)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            f"`{sch!r}` max len must be greater than or equal to 2, 1 given"
        )
