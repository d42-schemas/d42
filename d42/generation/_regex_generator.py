import string
import sys

if sys.version_info >= (3, 11):
    import re._parser as sre  # type: ignore
    from re._constants import (  # type: ignore
        ANY,
        AT,
        BRANCH,
        CATEGORY,
        CATEGORY_DIGIT,
        CATEGORY_WORD,
        IN,
        LITERAL,
        MAX_REPEAT,
        MAXREPEAT,
        MIN_REPEAT,
        NEGATE,
        NOT_LITERAL,
        RANGE,
        SUBPATTERN,
    )
else:
    import sre_parse as sre
    from sre_constants import (
        ANY,
        AT,
        BRANCH,
        CATEGORY,
        CATEGORY_DIGIT,
        CATEGORY_WORD,
        IN,
        LITERAL,
        MAX_REPEAT,
        MAXREPEAT,
        MIN_REPEAT,
        NEGATE,
        NOT_LITERAL,
        RANGE,
        SUBPATTERN,
    )

from typing import Any, Dict, List, Optional, Tuple

from ._random import Random

__all__ = ("RegexGenerator",)


class RegexGenerator:
    def __init__(self, random: Random, *,
                 alphabet: Optional[Dict[str, str]] = None,
                 max_repeat: int = 32) -> None:
        self._random = random
        self._alphabet = {
            "letters": string.ascii_letters + string.digits + string.punctuation + " ",
            "digits": string.digits,
            "word": string.ascii_letters + string.digits + "_",
        }
        if alphabet:
            self._alphabet.update(alphabet)
        self._max_repeat = max_repeat

    def _get_category_alphabet(self, value: Any) -> str:
        if value == CATEGORY_DIGIT:
            return self._alphabet["digits"]
        elif value == CATEGORY_WORD:
            return self._alphabet["word"]
        else:
            raise ValueError(f"Unknown category {value}")

    def _generate_any(self, value: None) -> str:
        return self._random.random_choice(self._alphabet["letters"])

    def _generate_literal(self, value: int) -> str:
        return chr(value)

    def _generate_in(self, value: List[Any]) -> str:
        (opcode, val), *other = value
        if opcode == NEGATE:
            return self._generate_not_in(other)

        opcode, val = self._random.random_choice(value)
        if opcode == RANGE:
            min_ord, max_ord = val
            ordinal = self._random.random_int(min_ord, max_ord)
            return self._generate_literal(ordinal)
        elif opcode == CATEGORY:
            alphabet = self._get_category_alphabet(val)
            return self._random.random_choice(alphabet)
        else:
            return self._generate(opcode, val)

    def _generate_not_in(self, value: List[Any]) -> str:
        exclude_letters = ""
        for opcode, val in value:
            if opcode == RANGE:
                min_ord, max_ord = val
                exclude_letters += "".join(self._generate_literal(x) for x in range(min_ord,
                                                                                    max_ord + 1))
            elif opcode == CATEGORY:
                exclude_letters += self._get_category_alphabet(val)
            else:
                exclude_letters += self._generate(opcode, val)

        letters = "".join(set(self._alphabet["letters"]) - set(exclude_letters))
        return self._random.random_choice(letters)

    def _generate_not_literal(self, value: int) -> str:
        return self._generate_not_in([(LITERAL, value)])

    def _generate_max_repeat(self, value: Tuple[int, int, List[Any]]) -> str:
        min_count, max_count, val = value
        if max_count in (MAX_REPEAT, MAXREPEAT):
            max_count = max(self._max_repeat, min_count)
        count = self._random.random_int(min_count, max_count)
        return "".join(self._generate_pattern(val) for _ in range(count))

    def _generate_min_repeat(self, value: Tuple[int, int, List[Any]]) -> str:
        return self._generate_max_repeat(value)

    def _generate_at(self, value: Any) -> str:
        return ""

    def _generate_branch(self, value: Tuple[None, Any]) -> str:
        none, val = value
        return self._generate_pattern(self._random.random_choice(val))

    def _generate_subpattern(self, value: Tuple[int, int, int, List[Any]]) -> str:
        group, add_flags, del_flags, subpattern = value
        return self._generate_pattern(subpattern)

    def _generate_pattern(self, value: List[Any]) -> str:
        return "".join(self._generate(*x) for x in value)

    def _generate(self, opcode: Any, value: Any) -> str:
        if opcode == ANY:
            return self._generate_any(value)
        elif opcode == LITERAL:
            return self._generate_literal(value)
        elif opcode == NOT_LITERAL:
            return self._generate_not_literal(value)
        elif opcode == IN:
            return self._generate_in(value)
        elif opcode == SUBPATTERN:
            return self._generate_subpattern(value)
        elif opcode == MAX_REPEAT:
            return self._generate_max_repeat(value)
        elif opcode == MIN_REPEAT:
            return self._generate_min_repeat(value)
        elif opcode == AT:
            return self._generate_at(value)
        elif opcode == BRANCH:
            return self._generate_branch(value)
        else:
            raise ValueError(f"Unknown opcode {opcode}")

    def generate(self, pattern: str) -> str:
        parsed = sre.parse(pattern)  # type: Any
        return self._generate_pattern(parsed)
