import pytest
from baby_steps import given, then, when
from pytest import raises

from d42 import optional as opt
from d42 import schema
from d42.declaration import DeclarationError
from d42.utils import make_required


def test_make_required_all_keys():
    with given:
        sch = schema.dict({
            "id": schema.int(42),
            opt("name"): schema.str("banana"),
            opt("created_at"): schema.int,
        })

    with when:
        res = make_required(sch)

    with then:
        assert res == schema.dict({
            "id": schema.int(42),
            "name": schema.str("banana"),
            "created_at": schema.int,
        })


def test_dict_one_key():
    with given:
        sch = schema.dict({
            "id": schema.int(42),
            opt("name"): schema.str("banana"),
            opt("created_at"): schema.int,
        })

    with when:
        res = make_required(sch, {"name"})

    with then:
        assert res == schema.dict({
            "id": schema.int(42),
            "name": schema.str("banana"),
            opt("created_at"): schema.int,
        })


def test_make_required_relaxed_dict():
    with given:
        sch = schema.dict({
            "id": schema.int(42),
            opt("name"): schema.str("banana"),
            opt("created_at"): schema.int,
            ...: ...
        })

    with when:
        res = make_required(sch)

    with then:
        assert res == schema.dict({
            "id": schema.int(42),
            "name": schema.str("banana"),
            "created_at": schema.int,
            ...: ...
        })


def test_make_required_one_key_relaxed_dict():
    with given:
        sch = schema.dict({
            "id": schema.int(42),
            opt("name"): schema.str("banana"),
            opt("created_at"): schema.int,
            ...: ...
        })

    with when:
        res = make_required(sch, {"name"})

    with then:
        assert res == schema.dict({
            "id": schema.int(42),
            "name": schema.str("banana"),
            opt("created_at"): schema.int,
            ...: ...
        })


@pytest.mark.parametrize("keys", [None, []])
def test_make_required_empty_dict(keys):
    with given:
        sch = schema.dict

    with when:
        res = make_required(sch, keys)

    with then:
        assert res == schema.dict


def test_make_required_invalid_schema_type_error():
    with given:
        sch = schema.list([schema.str("banana")])

    with when, raises(Exception) as exception:
        make_required(sch)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"Inappropriate type of schema {sch!r} ({type(sch)!r})"


def test_make_required_invalid_keys_type_error():
    with given:
        sch = schema.dict({
            "id": schema.int
        })

    with when, raises(Exception) as exception:
        make_required(sch, {"banana": "banana"})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("Inappropriate type of keys {'banana': 'banana'} "
                                        "(<class 'dict'>)")


def test_make_required_nonexisting_keys_error():
    with given:
        sch = schema.dict({
            "id": schema.int(42),
            opt("name"): schema.str("banana"),
        })

    with when, raises(Exception) as exception:
        make_required(sch, {"banana"})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "Nonexisting key 'banana'"


def test_make_required_empty_dict_nonexisting_keys_error():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        make_required(sch, {"banana"})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "Nonexisting key 'banana'"
