from datetime import date, timedelta

from baby_steps import given, then, when
from pytest import raises

from d42 import schema, substitute
from d42.substitution.errors import SubstitutionError


def test_date_substitution():
    with given:
        sch = schema.date
        value = date.today()

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.date(value)
        assert res != sch


def test_date_value_substitution():
    with given:
        value = date.today()
        sch = schema.date(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == sch == schema.date(value)
        assert id(res) != id(sch)


def test_date_substitution_invalid_value_error():
    with given:
        sch = schema.date

    with when, raises(Exception) as exception:
        substitute(sch, None)

    with then:
        assert exception.type is SubstitutionError


def test_date_substitution_incorrect_value_error():
    with given:
        value = date.today()
        sch = schema.date(value)

    with when, raises(Exception) as exception:
        substitute(sch, value + timedelta(days=1))

    with then:
        assert exception.type is SubstitutionError
