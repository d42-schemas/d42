from unittest.mock import call

from _pytest.python_api import raises
from baby_steps import given, then, when

from d42 import schema

from ..._fixtures import *  # noqa: F401, F403
from ..._utils import schema_mock


def test_empty_unique_list(*, generate):
    with given:
        sch = schema.list(schema.str).len(0).unique()

    with when:
        result = generate(sch)

    with then:
        assert result == []


def test_unique_list_with_choices(*, generate, generator, random_):
    with given:
        str_schema1 = schema_mock(return_value="test1")
        str_schema2 = schema_mock(return_value="test2")
        str_schema3 = schema_mock(return_value="test3")
        str_schema4 = schema_mock(return_value="test4")

        sch = schema.list([str_schema1, str_schema2, str_schema3, str_schema4]).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 4
        assert len(set(result)) == 4
        assert str_schema1.mock_calls == [call.__accept__(generator)]
        assert str_schema2.mock_calls == [call.__accept__(generator)]
        assert str_schema3.mock_calls == [call.__accept__(generator)]
        assert str_schema4.mock_calls == [call.__accept__(generator)]


def test_unique_list_numeric_range(*, generate, generator, random_):
    with given:
        int_schemas = [
            schema_mock(return_value=1),
            schema_mock(return_value=2),
            schema_mock(return_value=3),
            schema_mock(return_value=4),
            schema_mock(return_value=5)
        ]
        sch = schema.list(int_schemas).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 5
        assert len(set(result)) == 5
        for s in int_schemas:
            assert s.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_insufficient_range(*, generate, random_):
    with (given):
        random_.random_int.side_effect = \
            RuntimeError("Failed to generate a unique value after exhausting attempts")
        sch = schema.list(schema.int.min(1).max(3)).len(5).unique()

    with when, raises(RuntimeError) as exception:
        generate(sch)

    with then:
        assert "Failed to generate a unique value after exhausting attempts" in str(
            exception.value)
        assert random_.random_int.call_count >= 1


def test_unique_list_with_mixed_types(*, generate, generator):
    with given:
        str_schema = schema_mock(return_value="string1")
        int_schema = schema_mock(return_value=42)
        none_schema = schema_mock(return_value=None)
        str_schema2 = schema_mock(return_value="string2")
        int_schema2 = schema_mock(return_value=123)

        sch = schema.list([str_schema, int_schema, none_schema, str_schema2, int_schema2]).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 5
        assert len(set(map(str, result))) == 5
        assert str_schema.mock_calls == [call.__accept__(generator)]
        assert int_schema.mock_calls == [call.__accept__(generator)]
        assert none_schema.mock_calls == [call.__accept__(generator)]
        assert str_schema2.mock_calls == [call.__accept__(generator)]
        assert int_schema2.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_identical_elements(*, generate, generator):
    with given:
        int_schema1 = schema_mock(return_value=1)
        int_schema2 = schema_mock(return_value=1)
        sch = schema.list([int_schema1, int_schema2]).unique()

    with when, raises(RuntimeError) as exception:
        generate(sch)

    with then:
        assert "Failed to generate" in str(exception.value)
        assert len(int_schema1.mock_calls) >= 1


def test_unique_list_with_different_constraints(*, generate, generator):
    with given:
        int_schema1 = schema_mock(return_value=1)
        int_schema2 = schema_mock(return_value=3)
        sch = schema.list([int_schema1, int_schema2]).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 2
        assert len(set(result)) == 2
        assert int_schema1.mock_calls == [call.__accept__(generator)]
        assert int_schema2.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_custom_regex(*, generate, generator):
    with given:
        regex_schemas = [
            schema_mock(return_value='test123'),
            schema_mock(return_value='test456'),
            schema_mock(return_value='test789'),
            schema_mock(return_value='test012'),
            schema_mock(return_value='test345')
        ]

        sch = schema.list(regex_schemas).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 5
        assert len(set(result)) == 5
        for s in regex_schemas:
            assert s.mock_calls == [call.__accept__(generator)]


def test_unique_list_of_lists(*, generate, generator):
    with given:
        list_schema1 = schema_mock(return_value=[1, 2])
        list_schema2 = schema_mock(return_value=[3, 4])
        list_schema3 = schema_mock(return_value=[5, 1])

        sch = schema.list([list_schema1, list_schema2, list_schema3]).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 3
        assert len(set(str(item) for item in result)) == 3
        assert list_schema1.mock_calls == [call.__accept__(generator)]
        assert list_schema2.mock_calls == [call.__accept__(generator)]
        assert list_schema3.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_uuid(*, generate, generator):
    with given:
        from uuid import UUID
        uuid_schemas = [
            schema_mock(return_value=UUID('12345678-1234-4678-1234-567812345678')),
            schema_mock(return_value=UUID('87654321-4321-4678-4321-876543214321')),
            schema_mock(return_value=UUID('11111111-2222-4333-4444-555555555555')),
            schema_mock(return_value=UUID('99999999-8888-4777-6666-555555555555')),
            schema_mock(return_value=UUID('abcdefab-cdef-4abc-def1-abcdefabcdef')),
        ]

        sch = schema.list(uuid_schemas).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 5
        assert len(set(result)) == 5
        for s in uuid_schemas:
            assert s.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_internal_uniqueness(*, generate, generator):
    with given:
        list_schema1 = schema_mock(return_value=[1, 2, 3, 4, 5])
        list_schema2 = schema_mock(return_value=[6, 7, 8, 9, 10])
        list_schema3 = schema_mock(return_value=[2, 4, 6, 8, 10])

        sch = schema.list([list_schema1, list_schema2, list_schema3]).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 3
        assert len(set(str(item) for item in result)) == 3
        assert list_schema1.mock_calls == [call.__accept__(generator)]
        assert list_schema2.mock_calls == [call.__accept__(generator)]
        assert list_schema3.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_boolean_values(*, generate, generator):
    with given:
        bool_schema1 = schema_mock(return_value=True)
        bool_schema2 = schema_mock(return_value=False)

        sch = schema.list([bool_schema1, bool_schema2]).unique()

    with when:
        result = generate(sch)

    with then:
        assert sorted(result) == [False, True]
        assert len(set(result)) == 2
        assert bool_schema1.mock_calls == [call.__accept__(generator)]
        assert bool_schema2.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_datetime(*, generate, generator):
    with given:
        from datetime import datetime, timedelta
        base_date = datetime(2023, 1, 1)

        datetime_schemas = [
            schema_mock(return_value=base_date + timedelta(days=i))
            for i in range(5)
        ]

        sch = schema.list(datetime_schemas).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 5
        assert len(set(result)) == 5
        for s in datetime_schemas:
            assert s.mock_calls == [call.__accept__(generator)]


def test_unique_list_with_empty_elements(*, generate):
    with given:
        sch = schema.list([]).unique()

    with when:
        result = generate(sch)

    with then:
        assert result == []


def test_unique_list_with_any_schema(*, generate, generator):
    with given:
        schemas = [
            schema_mock(return_value="string1"),
            schema_mock(return_value=42),
            schema_mock(return_value=True),
            schema_mock(return_value="string2"),
            schema_mock(return_value=73),
            schema_mock(return_value=False),
            schema_mock(return_value="string3"),
            schema_mock(return_value=99),
            schema_mock(return_value="string4"),
            schema_mock(return_value=12)
        ]

        sch = schema.list(schemas).unique()

    with when:
        result = generate(sch)

    with then:
        assert len(result) == 10
        assert len(set(str(x) for x in result)) == 10
        for s in schemas:
            assert s.mock_calls == [call.__accept__(generator)]
