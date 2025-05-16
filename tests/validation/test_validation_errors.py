import uuid

from baby_steps import given, then, when
from th import PathHolder

from d42.declaration.types import IntSchema
from d42.validation.errors import (
    AlphabetValidationError,
    ExtraElementValidationError,
    ExtraKeyValidationError,
    InvalidUUIDVersionValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MaxValueValidationError,
    MinLengthValidationError,
    MinValueValidationError,
    MissingElementValidationError,
    MissingKeyValidationError,
    RegexValidationError,
    SchemaMismatchValidationError,
    SubstrValidationError,
    TypeValidationError,
    ValueValidationError,
)


def test_validation_type_error():
    with when:
        res = TypeValidationError(PathHolder(), "banana", int)

    with then:
        assert repr(res) == "TypeValidationError(PathHolder(), 'banana', <class 'int'>)"


def test_validation_value_error():
    with given:
        actual = "banana"
        expected = "cucumber"

    with when:
        res = ValueValidationError(PathHolder(), actual, expected)

    with then:
        assert repr(res) == "ValueValidationError(PathHolder(), 'banana', 'cucumber')"


def test_validation_min_value_error():
    with when:
        res = MinValueValidationError(PathHolder(), 41, 42)

    with then:
        assert repr(res) == "MinValueValidationError(PathHolder(), 41, 42)"


def test_validation_max_value_error():
    with when:
        res = MaxValueValidationError(PathHolder(), 43, 42)

    with then:
        assert repr(res) == "MaxValueValidationError(PathHolder(), 43, 42)"


def test_validation_len_error():
    with when:
        res = LengthValidationError(PathHolder(), "banana", 7)

    with then:
        assert repr(res) == "LengthValidationError(PathHolder(), 'banana', 7)"


def test_validation_min_len_error():
    with when:
        res = MinLengthValidationError(PathHolder(), "banana", 7)

    with then:
        assert repr(res) == "MinLengthValidationError(PathHolder(), 'banana', 7)"


def test_validation_max_len_error():
    with when:
        res = MaxLengthValidationError(PathHolder(), "banana", 7)

    with then:
        assert repr(res) == "MaxLengthValidationError(PathHolder(), 'banana', 7)"


def test_validation_alphabet_error():
    with when:
        res = AlphabetValidationError(PathHolder(), "banana!", "abn")

    with then:
        assert repr(res) == "AlphabetValidationError(PathHolder(), 'banana!', 'abn')"


def test_validation_substr_error():
    with when:
        res = SubstrValidationError(PathHolder(), "value", "substr")

    with then:
        assert repr(res) == "SubstrValidationError(PathHolder(), 'value', 'substr')"


def test_validation_regex_error():
    with when:
        res = RegexValidationError(PathHolder(), "value", ".*")

    with then:
        assert repr(res) == "RegexValidationError(PathHolder(), 'value', '.*')"


def test_validation_index_error():
    with when:
        res = MissingElementValidationError(PathHolder(), [], 0)

    with then:
        assert repr(res) == "MissingElementValidationError(PathHolder(), [], 0)"


def test_validation_extra_element_error():
    with when:
        res = ExtraElementValidationError(PathHolder(), [1], 0)

    with then:
        assert repr(res) == "ExtraElementValidationError(PathHolder(), [1], 0)"


def test_validation_missing__key_error():
    with when:
        res = MissingKeyValidationError(PathHolder(), {}, "key")

    with then:
        assert repr(res) == "MissingKeyValidationError(PathHolder(), {}, 'key')"


def test_validation_extra_key_error():
    with when:
        res = ExtraKeyValidationError(PathHolder(), {"key": "1"}, "key")

    with then:
        assert repr(res) == "ExtraKeyValidationError(PathHolder(), {'key': '1'}, 'key')"


def test_validation_schema_mismatch_error():
    with when:
        res = SchemaMismatchValidationError(
            PathHolder(),
            "key",
            (IntSchema(),),
            [(0, [TypeValidationError(PathHolder(), "key", int)])]
        )

    with then:
        assert repr(res) == (
            "SchemaMismatchValidationError(PathHolder(), 'key', (schema.int,), "
            "[(0, [TypeValidationError(PathHolder(), 'key', <class 'int'>)])])"
        )


def test_validation_invalid_uuid_version_error():
    with given:
        uuid5 = uuid.UUID("886313e1-3b8a-5372-9b90-0c9aee199e5d", version=5)

    with when:
        res = InvalidUUIDVersionValidationError(PathHolder(), uuid5, 5, 4)

    with then:
        assert repr(res) == ("InvalidUUIDVersionValidationError(PathHolder(), "
                             "UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d'), 5, 4)")
