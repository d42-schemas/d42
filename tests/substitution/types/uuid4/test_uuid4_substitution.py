import uuid
from uuid import uuid4, uuid5

from baby_steps import given, then, when
from pytest import raises

from d42 import schema, substitute
from d42.substitution.errors import SubstitutionError


def test_uuid4_substitution():
    with given:
        value = uuid4()
        sch = schema.uuid4

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.uuid4(value)
        assert res != sch


def test_uuid4_value_substitution():
    with given:
        value = uuid4()
        sch = schema.uuid4(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.uuid4(value)
        assert id(res) != id(sch)


def test_uuid4_substitution_invalid_value_error():
    with given:
        sch = schema.uuid4(uuid4())

    with when, raises(Exception) as exception:
        substitute(sch, str(uuid4()))

    with then:
        assert exception.type is SubstitutionError


def test_uuid4_substitution_incorrect_value_error():
    with given:
        sch = schema.uuid4(uuid4())

    with when, raises(Exception) as exception:
        substitute(sch, uuid4())

    with then:
        assert exception.type is SubstitutionError


def test_uuid4_substitution_incorrect_version_error():
    with given:
        sch = schema.uuid4
        uuid5_val = uuid5(uuid.NAMESPACE_DNS, "python.org")

    with when, raises(Exception) as exception:
        substitute(sch, uuid5_val)

    with then:
        assert exception.type is SubstitutionError
