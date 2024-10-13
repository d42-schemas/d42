from baby_steps import given, then, when
from pytest import raises

from d42 import optional, schema
from d42.declaration import DeclarationError


def test_dict_relaxed_empty_keys_declaration():
    with given:
        keys = {...: ...}

    with when:
        sch = schema.dict(keys)

    with then:
        assert sch.props.keys == {...: (..., False)}


def test_dict_relaxed_keys_declaration():
    with given:
        keys = {
            "id": schema.int(42),
            "name": schema.str("banana"),
            ...: ...
        }

    with when:
        sch = schema.dict(keys)

    with then:
        assert sch.props.keys == {key: (val, False) for key, val in keys.items()}


def test_dict_relaxed_optional_keys_declaration():
    with given:
        keys = {
            "id": schema.int(42),
            "name": schema.str("banana"),
            optional("created_at"): schema.int,
            ...: ...,
        }
        props = {
            "id": (schema.int(42), False),
            "name": (schema.str("banana"), False),
            "created_at": (schema.int, True),
            ...: (..., False),
        }

    with when:
        sch = schema.dict(keys)

    with then:
        assert sch.props.keys == props


def test_dict_relaxed_already_declared_declaration_error():
    with given:
        keys = {"key": schema.str}

    with when, raises(Exception) as exception:
        schema.dict({...: ...})(keys)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "`schema.dict({...: ...})` is already declared"


def test_dict_already_declared_relaxed_declaration_error():
    with given:
        keys = {"key": schema.str}

    with when, raises(Exception) as exception:
        schema.dict(keys)({...: ...})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "\n".join([
            "`schema.dict({",
            "    'key': schema.str",
            "})` is already declared",
        ])


def test_dict_relaxed_invalid_key_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.dict({"key": ...})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "Inappropriate type of key 'key' (<class 'str'>)"


def test_dict_relaxed_invalid_val_type_declaration_error():
    with when, raises(Exception) as exception:
        schema.dict({...: "val"})

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == "Inappropriate type of value 'val' (<class 'str'>)"
