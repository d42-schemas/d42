from datetime import date, datetime
from uuid import uuid4

from baby_steps import given, then, when
from pytest import raises

from d42 import schema
from d42.utils import from_native


def test_none_value():
    with when:
        res = from_native(None)

    with then:
        assert res == schema.none


def test_bool_value():
    with given:
        value = True

    with when:
        res = from_native(value)

    with then:
        assert res == schema.bool(value)


def test_int_value():
    with given:
        value = 42

    with when:
        res = from_native(value)

    with then:
        assert res == schema.int(value)


def test_float_value():
    with given:
        value = 3.14

    with when:
        res = from_native(value)

    with then:
        assert res == schema.float(value)


def test_str_value():
    with given:
        value = "banana"

    with when:
        res = from_native(value)

    with then:
        assert res == schema.str(value)


def test_list_empty_value():
    with given:
        value = []

    with when:
        res = from_native(value)

    with then:
        assert res == schema.list(value)


def test_list_value():
    with given:
        value = [1, 2, 3]

    with when:
        res = from_native(value)

    with then:
        assert res == schema.list([schema.int(1), schema.int(2), schema.int(3)])


def test_dict_empty_value():
    with given:
        value = {}

    with when:
        res = from_native(value)

    with then:
        assert res == schema.dict(value)


def test_dict_value():
    with given:
        value = {
            "id": 1,
            "name": "Bob"
        }

    with when:
        res = from_native(value)

    with then:
        assert res == schema.dict({
            "id": schema.int(1),
            "name": schema.str("Bob"),
        })


def test_bytes_value():
    with given:
        value = b""

    with when:
        res = from_native(value)

    with then:
        assert res == schema.bytes(value)


def test_uuid4_value():
    with given:
        value = uuid4()

    with when:
        res = from_native(value)

    with then:
        assert res == schema.uuid4(value)


def test_date_value():
    with given:
        value = date.today()

    with when:
        res = from_native(value)

    with then:
        assert res == schema.date(value)


def test_datetime_value():
    with given:
        value = datetime.now()

    with when:
        res = from_native(value)

    with then:
        assert res == schema.datetime(value)


def test_unknown_value():
    with given:
        value = Exception()

    with when, raises(Exception) as exception:
        from_native(value)

    with then:
        assert exception.type is ValueError
