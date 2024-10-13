from datetime import datetime, timedelta

from baby_steps import given, then, when
from pytest import raises

from d42 import schema, substitute
from d42.substitution.errors import SubstitutionError


def test_datetime_substitution():
    with given:
        sch = schema.datetime
        value = datetime.now()

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.datetime(value)
        assert res != sch


def test_datetime_value_substitution():
    with given:
        value = datetime.now()
        sch = schema.datetime(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == sch == schema.datetime(value)
        assert id(res) != id(sch)


def test_datetime_substitution_invalid_value_error():
    with given:
        sch = schema.datetime

    with when, raises(Exception) as exception:
        substitute(sch, None)

    with then:
        assert exception.type is SubstitutionError


def test_datetime_substitution_incorrect_value_error():
    with given:
        value = datetime.now()
        sch = schema.datetime(value)

    with when, raises(Exception) as exception:
        substitute(sch, value + timedelta(days=1))

    with then:
        assert exception.type is SubstitutionError
