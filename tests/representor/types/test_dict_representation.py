from baby_steps import given, then, when

from d42 import optional, schema
from d42.representation import represent


def test_dict_representation():
    with given:
        sch = schema.dict

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.dict"


def test_dict_empty_representation():
    with given:
        sch = schema.dict({})

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.dict({})"


def test_dict_one_key_representation():
    with given:
        sch = schema.dict({"id": schema.int})

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.dict({",
            "    'id': schema.int",
            "})"
        ])


def test_dict_many_keys_representation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str("banana")
        })

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.dict({",
            "    'id': schema.int,",
            "    'name': schema.str('banana')",
            "})",
        ])


def test_dict_optional_key_representation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("name"): schema.str,
        })

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.dict({",
            "    'id': schema.int,",
            "    optional('name'): schema.str",
            "})"
        ])


def test_dict_nested_keys_representation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "user": schema.dict({
                "id": schema.int,
                "name": schema.str("banana")
            }),
            "is_deleted": schema.bool
        })

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.dict({",
            "    'id': schema.int,",
            "    'user': schema.dict({",
            "        'id': schema.int,",
            "        'name': schema.str('banana')",
            "    }),",
            "    'is_deleted': schema.bool",
            "})",
        ])


def test_dict_relaxed_empty_representation():
    with given:
        sch = schema.dict({...: ...})

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.dict({...: ...})"


def test_dict_relaxed_one_key_representation():
    with given:
        sch = schema.dict({"id": schema.int, ...: ...})

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.dict({",
            "    'id': schema.int,",
            "    ...: ...",
            "})",
        ])


def test_dict_relaxed_many_keys_representation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            "name": schema.str("banana"),
            ...: ...,
        })

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.dict({",
            "    'id': schema.int,",
            "    'name': schema.str('banana'),",
            "    ...: ...",
            "})",
        ])
