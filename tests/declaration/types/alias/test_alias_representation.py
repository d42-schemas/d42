from baby_steps import given, then, when

from d42 import schema
from d42.declaration.types import TypeAliasSchema
from d42.representor import represent


def test_alias_default_representation():
    with given:
        sch = TypeAliasSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "TypeAliasSchema<schema.any>"


def test_alias_representation():
    with given:
        smth_schema = schema.alias("smth_schema", schema.any)

    with when:
        res = represent(smth_schema)

    with then:
        assert res == "smth_schema<schema.any>"


def test_alias_in_alias_representation():
    with given:
        smth_schema = schema.alias("smth_schema", schema.any)
        tmp_schema = schema.alias("tmp_schema", smth_schema)

    with when:
        res = represent(tmp_schema)

    with then:
        assert res == "tmp_schema<smth_schema<schema.any>>"


def test_alias_nested_representation():
    with given:
        user_schema = schema.dict({"id": schema.int, "name": schema.str})
        sch = schema.alias("user_list_schema", schema.list([user_schema]))

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "user_list_schema<schema.list([",
            "    schema.dict({",
            "        'id': schema.int,",
            "        'name': schema.str",
            "    })",
            "])>",
        ])
