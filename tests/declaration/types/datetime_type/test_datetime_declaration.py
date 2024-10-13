from datetime import datetime, timedelta

from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.declaration import DeclarationError
from d42.declaration.types import DateTimeSchema


def test_datetime_declaration():
    with when:
        sch = schema.datetime

    with then:
        assert isinstance(sch, DateTimeSchema)


def test_datetime_value_declaration():
    with given:
        value = datetime.now()

    with when:
        sch = schema.datetime(value)

    with then:
        assert sch.props.value == value


def test_datetime_invalid_value_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.datetime(timedelta())

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == (
            "`schema.datetime` value must be an instance of 'datetime', "
            "instance of 'timedelta' datetime.timedelta(0) given"
        )


def test_datetime_already_declared_declaration_error():
    with given:
        dt = datetime.now()

    with when, raises(Exception) as exception:
        schema.datetime(dt)(dt)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`schema.datetime({dt!r})` is already declared"
