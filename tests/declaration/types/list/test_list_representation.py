from baby_steps import given, then, when

from d42 import schema
from d42.representor import represent


def test_list_representation():
    with given:
        sch = schema.list

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list"


def test_list_empty_representation():
    with given:
        sch = schema.list([])

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list([])"


def test_list_one_element_representation():
    with given:
        sch = schema.list([
            schema.int
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    schema.int",
            "])"
        ])


def test_list_many_elements_representation():
    with given:
        sch = schema.list([
            schema.bool,
            schema.int(1),
            schema.str("banana")
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    schema.bool,",
            "    schema.int(1),",
            "    schema.str('banana')",
            "])"
        ])


def test_list_nested_elements_representation():
    with given:
        sch = schema.list([
            schema.int,
            schema.list([
                schema.int(1),
                schema.int(2),
            ]),
            schema.int
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    schema.int,",
            "    schema.list([",
            "        schema.int(1),",
            "        schema.int(2)",
            "    ]),",
            "    schema.int",
            "])"
        ])


def test_list_contains_no_elements_representation():
    with given:
        sch = schema.list([
            ...
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    ...",
            "])",
        ])


def test_list_contains_body_elements_representation():
    with given:
        sch = schema.list([
            ...,
            schema.int(1),
            schema.int(2),
            ...
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    ...,",
            "    schema.int(1),",
            "    schema.int(2),",
            "    ...",
            "])",
        ])


def test_list_contains_head_elements_representation():
    with given:
        sch = schema.list([
            schema.int(1),
            schema.int(2),
            ...
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    schema.int(1),",
            "    schema.int(2),",
            "    ...",
            "])"
        ])


def test_list_contains_tail_elements_representation():
    with given:
        sch = schema.list([
            ...,
            schema.int(1),
            schema.int(2)
        ])

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "schema.list([",
            "    ...,",
            "    schema.int(1),",
            "    schema.int(2)",
            "])"
        ])


def test_list_len_representation():
    with given:
        sch = schema.list.len(10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list.len(10)"


def test_list_min_len_representation():
    with given:
        sch = schema.list.len(1, ...)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list.len(1, ...)"


def test_list_max_len_representation():
    with given:
        sch = schema.list.len(..., 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list.len(..., 10)"


def test_list_min_max_len_representation():
    with given:
        sch = schema.list.len(1, 10)

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.list.len(1, 10)"
