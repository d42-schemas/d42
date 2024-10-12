from datetime import date, timedelta

from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import DateSchema


def test_date_declaration():
    with when:
        sch = schema.date

    with then:
        assert isinstance(sch, DateSchema)


def test_date_value_declaration():
    with given:
        value = date.today()

    with when:
        sch = schema.date(value)

    with then:
        assert sch.props.value == value


def test_date_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.date(timedelta())

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.date` value must be an instance of 'date', "
            "instance of 'timedelta' datetime.timedelta(0) given"
        )


def test_date_already_declared_declaration_error():
    with given:
        dt = date.today()

    with when, raises(Exception) as exception:
        schema.date(dt)(dt)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`schema.date({dt!r})` is already declared"
