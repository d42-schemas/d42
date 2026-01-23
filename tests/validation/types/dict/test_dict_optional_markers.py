from baby_steps import given, then, when
from th import PathHolder

from d42 import optional, schema
from d42.substitution import substitute
from d42.validation import validate
from d42.validation.errors import (
    MissingKeyValidationError,
    TypeValidationError,
    UnexpectedKeyValidationError,
)


def test_dict_optional_absent_validation():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("deleted_at"): schema.int
        })
        sch_with_absent = substitute(sch, {
            "id": 1,
            "deleted_at": optional.absent
        })

    with when:
        result = validate(sch_with_absent, {"id": 1})

    with then:
        assert result.get_errors() == []


def test_dict_optional_absent_validation_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
            optional("deleted_at"): schema.int
        })
        sch_with_absent = substitute(sch, {
            "id": 1,
            "deleted_at": optional.absent
        })

    with when:
        result = validate(sch_with_absent, {"id": 1, "deleted_at": 123})

    with then:
        assert result.get_errors() == [
            UnexpectedKeyValidationError(PathHolder(), {"id": 1, "deleted_at": 123}, "deleted_at")
        ]


def test_dict_optional_present_key_validation():
    with given:
        sch = schema.dict({
            "name": schema.str,
            optional("age"): schema.int
        })
        sch_with_present = substitute(sch, {
            "name": "Alice",
            "age": optional.present
        })

    with when:
        result = validate(sch_with_present, {"name": "Alice", "age": 42})

    with then:
        assert result.get_errors() == []


def test_dict_optional_present_missing_key_validation_error():
    with given:
        sch = schema.dict({
            "name": schema.str,
            optional("age"): schema.int
        })
        sch_with_present = substitute(sch, {
            "name": "Alice",
            "age": optional.present
        })
        value = {"name": "Alice"}

    with when:
        result = validate(sch_with_present, value)

    with then:
        assert result.get_errors() == [
            MissingKeyValidationError(PathHolder(), value, "age")
        ]


def test_dict_optional_present_key_type_validation_error():
    with given:
        sch = schema.dict({
            "name": schema.str,
            optional("age"): schema.int
        })
        sch_with_present = substitute(sch, {
            "name": "Alice",
            "age": optional.present
        })
        value = {"name": "Alice", "age": "123"}

    with when:
        result = validate(sch_with_present, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder()["age"], value["age"], int)
        ]


def test_dict_nested_optional_present_validation():
    with given:
        sch = schema.dict({
            "users": schema.list(schema.dict({
                "id": schema.int,
                optional("name"): schema.str
            }))
        })
        sch_with_present = substitute(sch, {
            "users": [
                {
                    "id": 1,
                    "name": optional.present
                }
            ]
        })

    with when:
        result = validate(sch_with_present, {"users": [{"id": 1, "name": "Alice"}]})

    with then:
        assert result.get_errors() == []


def test_dict_nested_optional_present_missing_key_validation_error():
    with given:
        sch = schema.dict({
            "users": schema.list(schema.dict({
                "id": schema.int,
                optional("name"): schema.str
            }))
        })
        sch_with_present = substitute(sch, {
            "users": [
                {
                    "id": 1,
                    "name": optional.present
                }
            ]
        })
        value = {"users": [{"id": 1}]}

    with when:
        result = validate(sch_with_present, value)

    with then:
        assert result.get_errors() == [
            MissingKeyValidationError(PathHolder()["users"][0], value["users"][0], "name")
        ]
