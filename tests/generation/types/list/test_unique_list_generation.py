from _pytest.python_api import raises
from baby_steps import given, then, when

from d42 import fake, schema


def test_fake_empty_unique_list():
    with given:
        sch = schema.list(schema.str).len(0).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 0


def test_fake_unique_list_with_choices():
    with given:
        sch = schema.list(
            schema.str('test1') |
            schema.str('test2') |
            schema.str('test3') |
            schema.str('test4')
        ).len(4).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 4
        assert len(set(result)) == 4
        assert all(val in ['test1', 'test2', 'test3', 'test4'] for val in result)


def test_fake_unique_list_numeric_range():
    with given:
        sch = schema.list(schema.int.min(1).max(10)).len(5).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 5
        assert len(set(result)) == 5
        assert all(1 <= val <= 10 for val in result)


def test_fake_unique_list_with_insufficient_range():
    with given:
        sch = schema.list(schema.int.min(1).max(3)).len(5).unique()

    with when, raises(RuntimeError) as exception:
        fake(sch)

    with then:
        assert "Failed to generate" in str(exception.value)


def test_fake_unique_list_with_mixed_types():
    with given:
        sch = schema.list(schema.str | schema.int | schema.none).len(5).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 5
        assert len(set(map(str, result))) == 5


def test_fake_unique_list_with_identical_elements():
    with given:
        sch = schema.list([schema.int(1), schema.int(1)]).unique()

    with when, raises(RuntimeError) as exception:
        fake(sch)

    with then:
        assert ("Failed to generate" in str(exception.value) or
                "Cannot generate" in str(exception.value))


def test_fake_unique_list_with_different_constraints():
    with given:
        sch = schema.list([schema.int.min(1).max(2), schema.int.min(3).max(4)]).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 2
        assert len(set(result)) == 2
        assert 1 <= result[0] <= 2
        assert 3 <= result[1] <= 4


def test_fake_list_fixed_length():
    with given:
        fixed_length = 7
        sch = schema.list(schema.int).len(fixed_length)

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == fixed_length
        assert all(isinstance(item, int) for item in result)


def test_fake_unique_list_with_custom_regex():
    with given:
        sch = schema.list(schema.str.regex(r'test\d{3}')).len(5).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 5
        assert len(set(result)) == 5
        assert all(item.startswith('test') and len(item) == 7 for item in result)


def test_fake_unique_list_of_lists():
    with given:
        sch = schema.list(schema.list(schema.int.min(1).max(5)).len(2)).len(3).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, list) and len(item) == 2 for item in result)
        assert all(1 <= x <= 5 for item in result for x in item)
        assert len(set(str(item) for item in result)) == 3


def test_fake_nested_lists_with_uniqueness():
    with given:
        sch = schema.list(
            schema.list(schema.int.min(1).max(10)).len(3).unique()
        ).len(2)

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, list) and len(item) == 3 for item in result)
        assert all(len(set(inner_list)) == 3 for inner_list in result)


def test_fake_unique_list_with_uuid():
    with given:
        sch = schema.list(schema.uuid4).len(5).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 5
        assert len(set(result)) == 5


def test_fake_non_unique_list_with_duplicates():
    with given:
        sch = schema.list([schema.int(42), schema.int(42), schema.int(42)]).len(3)

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(item == 42 for item in result)


def test_fake_list_with_none_elements():
    with given:
        sch = schema.list([schema.none, schema.none, schema.none])

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(item is None for item in result)


def test_fake_unique_list_with_internal_uniqueness():
    with given:
        sch = schema.list(
            schema.list(schema.int.min(1).max(10)).len(5).unique()
        ).len(3).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 3
        assert len(set(str(item) for item in result)) == 3
        assert all(len(set(inner_list)) == 5 for inner_list in result)


def test_fake_unique_list_with_min_max_len():
    with given:
        max_len = 7
        sch = schema.list(schema.int.min(1).max(20)).len(..., max_len).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) <= max_len
        assert len(set(result)) == len(result)


def test_fake_unique_list_with_min_len():
    with given:
        min_len = 5
        sch = schema.list(schema.int.min(1).max(100)).len(min_len, ...).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) >= min_len
        assert len(set(result)) == len(result)


def test_fake_unique_list_with_boolean_values():
    with given:
        sch = schema.list(schema.bool).len(2).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 2
        assert len(set(result)) == 2
        assert True in result
        assert False in result


def test_fake_unique_list_with_datetime():
    with given:
        sch = schema.list(schema.datetime).len(5).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 5
        assert len(set(result)) == 5


def test_fake_unique_list_with_empty_elements():
    with given:
        sch = schema.list([]).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 0


def test_fake_unique_list_with_any_schema():
    with given:
        sch = schema.list(schema.any(
            schema.str,
            schema.int.min(1).max(100),
            schema.bool
        )).len(10).unique()

    with when:
        result = fake(sch)

    with then:
        assert isinstance(result, list)
        assert len(result) == 10
        assert len(set(str(x) for x in result)) == 10
