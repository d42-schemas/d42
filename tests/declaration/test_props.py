from baby_steps import given, then, when
from niltype import Nil

from d42.declaration import Props


def test_props_set():
    with given:
        props = Props()

    with when:
        res = props.set("key", "val")

    with then:
        assert isinstance(res, Props)
        assert res != props


def test_props_update():
    with given:
        props = Props()

    with when:
        res = props.update(key1="val1", key2="val2")

    with then:
        assert isinstance(res, Props)
        assert res != props


def test_props_get_default():
    with given:
        props = Props()

    with when:
        res = props.get("non_existing")

    with then:
        assert res is Nil


def test_props_get_custom_default():
    with given:
        props = Props()

    with when:
        res = props.get("non_existing", None)

    with then:
        assert res is None


def test_get_setted():
    with given:
        key, val = "key", "val"
        props = Props().set(key, val)

    with when:
        res = props.get("key")

    with then:
        assert res == val


def test_get_updated():
    with given:
        props = Props().update(key1="val1", key2="val2")

    with when:
        res = props.get("key1")

    with then:
        assert res == "val1"


def test_props_repr():
    with given:
        props = Props()

    with when:
        res = repr(props)

    with then:
        assert res == "<Props {}>"


def test_props_eq_empty():
    with given:
        props1 = Props()
        props2 = Props()

    with when:
        res = props1 == props2

    with then:
        assert res is True


def test_props_eq_updated():
    with given:
        props1 = Props().update(key1="val1", key2="val2")
        props2 = Props().update(key1="val1", key2="val2")

    with when:
        res = props1 == props2

    with then:
        assert res is True


def test_props_not_eq_incorrect_other():
    with given:
        props1 = Props().update(key1="val1", key2="val2")

    with when:
        res = props1 == "Props()"

    with then:
        assert res is False


def test_props_not_eq_less_other():
    with given:
        props1 = Props().update(key1="val1", key2="val2")
        props2 = Props().update(key1="val1")

    with when:
        res = props1 == props2

    with then:
        assert res is False


def test_props_not_eq_more_other():
    with given:
        props1 = Props().update(key1="val1")
        props2 = Props().update(key1="val1", key2="val2")

    with when:
        res = props1 == props2

    with then:
        assert res is False


def test_props_no_keys():
    with given:
        props = Props()

    with when:
        keys = [key for key in props]

    with then:
        assert keys == []


def test_props_keys():
    with given:
        props = Props().update(key1="val1", key2="val2")

    with when:
        keys = [key for key in props]

    with then:
        assert keys == ["key1", "key2"]
