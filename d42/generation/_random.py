import random
from typing import Any, List, Sequence, TypeVar, cast

from niltype import Nil, Nilable

__all__ = ("Random",)

_T = TypeVar("_T")
SeedType = TypeVar("SeedType", int, float, str, bytes, bytearray)


class Random:
    def set_seed(self, seed: SeedType) -> None:
        random.seed(seed)

    def random_int(self, start: int, end: int) -> int:
        return random.randint(start, end)

    def random_float(self, start: float, end: float, precision: Nilable[int] = Nil) -> float:
        if start > end:
            raise ValueError("random_float: start must be <= end")

        if precision is Nil:
            return random.uniform(start, end)

        scale_factor = 10 ** precision
        left_number = int(start * scale_factor)
        right_number = int(end * scale_factor)

        result = cast(float, self.random_int(left_number, right_number) / scale_factor)
        return round(result, precision)

    def random_str(self, length: int, alphabet: str) -> str:
        return "".join(random.choice(alphabet) for _ in range(length))

    def random_choice(self, sequence: Sequence[_T]) -> _T:
        return random.choice(sequence)

    def shuffle_list(self, elements: List[Any]) -> None:
        random.shuffle(elements)
