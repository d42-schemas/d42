from _pytest.python_api import raises
from baby_steps import given, then, when

from d42 import optional
from d42.utils import rollout


def test_rollout_empty():
    with given:
        val = {}

    with when:
        res = rollout(val)

    with then:
        assert res == {}


def test_rollout_flat():
    with given:
        val = {
            "id": 1,
            "name": "Bob"
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "id": 1,
            "name": "Bob"
        }


def test_rollout_nested():
    with given:
        val = {
            "id": 1,
            "name": "Bob",
            "friend.id": 2,
            "friend.name": "Alice",
            optional("deleted_at"): None
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "id": 1,
            "name": "Bob",
            "friend": {
                "id": 2,
                "name": "Alice"
            },
            optional("deleted_at"): None
        }


def test_rollout_nested_with_empty_keys():
    with given:
        val = {
            "result...id": 1,
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {"result": {"": {"": {"id": 1}}}}


def test_rollout_deep_nested():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            "result.friend.id": 2,
            "result.friend.name": "Alice",
            optional("result.friend.deleted_at"): None
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                "id": 1,
                "name": "Bob",
                "friend": {
                    "id": 2,
                    "name": "Alice",
                    optional("deleted_at"): None
                }
            }
        }


def test_rollout_deep_nested_dict():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            "result.friend": {
                "id": 2
            },
            "result.friend.name": "Alice",
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                "id": 1,
                "name": "Bob",
                "friend": {
                    "id": 2,
                    "name": "Alice"
                }
            }
        }


def test_rollout_non_str_key():
    with given:
        val = {
            "result.id": 1,
            None: None,
        }

    with when, raises(Exception) as exception:
        rollout(val)

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == "Unexpected key type <class 'NoneType'>"


def test_rollout_non_str_optioal_key():
    with given:
        val = {
            "result.id": 1,
            optional(None): None,
        }

    with when, raises(Exception) as exception:
        rollout(val)

    with then:
        assert exception.type is TypeError
        assert str(exception.value) == "Unexpected key type <class 'NoneType'>"


def test_rollout_relaxed():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            ...: ...
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                "id": 1,
                "name": "Bob",
            },
            ...: ...
        }


def test_rollout_ellipsis_key():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            ...: None
        }

    with when, raises(Exception) as exception:
        rollout(val)

    with then:
        assert exception.type is ValueError
        assert str(exception.value) == "Expected both key and value to be ellipsis"


def test_rollout_nested_relaxed():
    with given:
        val = {
            "result": {...: ...},
            "result.id": 1,
            "result.name": "Bob",
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                ...: ...,
                "id": 1,
                "name": "Bob",
            }
        }


def test_rollout_deep_nested_relaxed():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            "result.friend": {
                "id": 2,
                ...: ...
            },
            "result.friend.name": "Alice",
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                "id": 1,
                "name": "Bob",
                "friend": {
                    "id": 2,
                    "name": "Alice",
                    ...: ...
                }
            }
        }
