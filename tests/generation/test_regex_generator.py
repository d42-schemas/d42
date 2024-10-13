import string
import sys

if sys.version_info >= (3, 11):
    from re._constants import CATEGORY, CATEGORY_DIGIT, CATEGORY_WORD, LITERAL, RANGE
else:
    from sre_constants import CATEGORY, CATEGORY_DIGIT, CATEGORY_WORD, LITERAL, RANGE
from typing import Dict, Optional
from unittest.mock import Mock, call

import pytest
from baby_steps import given, then, when
from pytest import raises

from d42.generation import Random, RegexGenerator

from ._fixtures import *  # noqa: F401, F403


def make_generator(random: Random, *,
                   alphabet: Dict[str, str] = None,
                   max_repeat: Optional[int] = None) -> RegexGenerator:
    return RegexGenerator(random, alphabet=alphabet, max_repeat=max_repeat)


def test_any(*, random_: Mock):
    with given:
        alphabet = string.ascii_lowercase
        generator = make_generator(random_, alphabet={"letters": alphabet})

    with when:
        res = generator.generate(r".")

    with then:
        assert res in alphabet
        assert random_.mock_calls == [
            call.random_choice(alphabet)
        ]


def test_literal(*, regex_generator: RegexGenerator, random_: Mock):
    with when:
        res = regex_generator.generate(r"a")

    with then:
        assert res == "a"
        assert random_.mock_calls == []


def test_range(*, regex_generator: RegexGenerator, random_: Mock):
    with given:
        alphabet = string.digits
        alphabet_range = (ord("0"), ord("9"))

    with when:
        res = regex_generator.generate(r"[0-9]")

    with then:
        assert res in alphabet
        assert random_.mock_calls == [
            call.random_choice([(RANGE, alphabet_range)]),
            call.random_int(*alphabet_range),
        ]


def test_in(*, regex_generator: RegexGenerator, random_: Mock):
    with given:
        alphabet = "ab"

    with when:
        res = regex_generator.generate(r"[ab]")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice([
                (LITERAL, ord(alphabet[0])),
                (LITERAL, ord(alphabet[-1]))
            ])
        ]


def test_negate(*, random_: Mock):
    with given:
        letters = string.ascii_lowercase
        alphabet = "".join(set(letters) - set("ab"))
        generator = make_generator(random_, alphabet={"letters": letters})

    with when:
        res = generator.generate(r"[^ab]")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice(alphabet)
        ]


def test_negate_category(*, random_: Mock):
    with given:
        letters = string.ascii_lowercase + string.digits
        alphabet = "".join(set(letters) - set(string.digits))
        generator = make_generator(random_, alphabet={"letters": letters})

    with when:
        res = generator.generate(r"[^\d]")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice(alphabet)
        ]


def test_negate_range(*, random_: Mock):
    with given:
        letters = string.ascii_lowercase + string.digits
        alphabet = "".join(set(letters) - set(string.digits))
        generator = make_generator(random_, alphabet={"letters": letters})

    with when:
        res = generator.generate(r"[^0-9]")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice(alphabet)
        ]


def test_not_literal(*, random_: Mock):
    with given:
        letters = string.ascii_lowercase
        alphabet = "".join(set(string.ascii_lowercase) - set("a"))
        generator = make_generator(random_, alphabet={"letters": letters})

    with when:
        res = generator.generate(r"[^a]")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice(alphabet)
        ]


def test_max_repeat(*, random_: Mock):
    with given:
        repeat = 3
        max_repeat = 10
        generator = make_generator(random_, max_repeat=max_repeat)
        random_.random_int = Mock(return_value=repeat)

    with when:
        res = generator.generate(r"a+")

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(1, max_repeat)
        ]


def test_min_repeat(*, random_: Mock):
    with given:
        repeat = 3
        max_repeat = 10
        generator = make_generator(random_, max_repeat=max_repeat)
        random_.random_int = Mock(return_value=repeat)

    with when:
        res = generator.generate(r"a+?")

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(1, max_repeat)
        ]


def test_repeat_exact(*, random_: Mock):
    with given:
        max_repeat = 10
        repeat = max_repeat + 1
        generator = make_generator(random_, max_repeat=max_repeat)
        random_.random_int = Mock(return_value=repeat)

    with when:
        res = generator.generate(r"a{11}")

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(repeat, repeat)
        ]


def test_repeat_min(*, random_: Mock):
    with given:
        max_repeat = 10
        repeat = max_repeat + 1
        generator = make_generator(random_, max_repeat=max_repeat)
        random_.random_int = Mock(return_value=repeat)

    with when:
        res = generator.generate(r"a{11,}")

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(repeat, repeat)
        ]


def test_repeat_max(*, random_: Mock):
    with given:
        max_repeat = 10
        repeat = max_repeat + 1
        generator = make_generator(random_, max_repeat=max_repeat)
        random_.random_int = Mock(return_value=repeat)

    with when:
        res = generator.generate(r"a{,11}")

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(0, repeat)
        ]


def test_repeat_range(*, random_: Mock):
    with given:
        repeat = 12
        max_repeat = 10
        generator = make_generator(random_, max_repeat=max_repeat)
        random_.random_int = Mock(return_value=repeat)

    with when:
        res = generator.generate(r"a{11,13}")

    with then:
        assert res == "a" * repeat
        assert random_.mock_calls == [
            call.random_int(11, 13)
        ]


@pytest.mark.parametrize("pattern", [
    r"^",
    r"$",
])
def test_at(pattern: str, *, regex_generator: RegexGenerator, random_: Mock):
    with when:
        res = regex_generator.generate(pattern)

    with then:
        assert res == ""
        assert random_.mock_calls == []


def test_branch(*, regex_generator: RegexGenerator, random_: Mock):
    with when:
        res = regex_generator.generate(r"ab|bc")

    with then:
        assert res in ("ab", "bc")
        random_.random_choice.assert_called_once()
        # sre_parse.SubPattern to list
        arg = [list(x) for x in random_.mock_calls[0].args[0]]
        assert arg == [
            [(LITERAL, ord("a")), (LITERAL, ord("b"))],
            [(LITERAL, ord("b")), (LITERAL, ord("c"))]
        ]


def test_subpattern(*, regex_generator: RegexGenerator, random_: Mock):
    with when:
        res = regex_generator.generate(r"(ab)")

    with then:
        assert res == "ab"
        assert random_.mock_calls == []


def test_category_digit(*, random_: Mock):
    with given:
        alphabet = string.digits
        generator = make_generator(random_, alphabet={"digits": alphabet})

    with when:
        res = generator.generate(r"\d")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice([(CATEGORY, CATEGORY_DIGIT)]),
            call.random_choice(alphabet)
        ]


def test_category_word(*, random_: Mock):
    with given:
        alphabet = string.ascii_letters
        generator = make_generator(random_, alphabet={"word": alphabet})

    with when:
        res = generator.generate(r"\w")

    with then:
        assert res in set(alphabet)
        assert random_.mock_calls == [
            call.random_choice([(CATEGORY, CATEGORY_WORD)]),
            call.random_choice(alphabet)
        ]


def test_unknown_opcode(*, regex_generator: RegexGenerator, random_: Mock):
    with when, raises(Exception) as exception:
        regex_generator.generate(r"(?P<quote>[']).*?(?P=quote)")

    with then:
        assert exception.type is ValueError
        assert str(exception.value) == "Unknown opcode GROUPREF"


def test_unknown_category(*, regex_generator: RegexGenerator, random_: Mock):
    with when, raises(Exception) as exception:
        regex_generator.generate(r"\W")

    with then:
        assert exception.type is ValueError
        assert str(exception.value) == "Unknown category CATEGORY_NOT_WORD"
