import sys
from datetime import date, datetime, timedelta
from typing import Any, Callable, Dict, List, Set
from uuid import UUID, uuid4

from niltype import Nil

from d42.declaration import GenericSchema, SchemaVisitor
from d42.declaration.types import (
    AnySchema,
    BoolSchema,
    BytesSchema,
    DateSchema,
    DateTimeSchema,
    DictSchema,
    FloatSchema,
    GenericTypeAliasSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    TypeAliasPropsType,
    UUID4Schema,
)
from d42.utils import is_ellipsis

from ._consts import (
    BYTES_LEN_MAX,
    BYTES_LEN_MIN,
    FLOAT_MAX,
    FLOAT_MIN,
    INT_MAX,
    INT_MIN,
    LIST_LEN_MAX,
    LIST_LEN_MIN,
    STR_ALPHABET,
    STR_LEN_MAX,
    STR_LEN_MIN,
)
from ._random import Random
from ._regex_generator import RegexGenerator

__all__ = ("Generator",)


class Generator(SchemaVisitor[Any]):
    def __init__(self, random: Random, regex_generator: RegexGenerator) -> None:
        self._random = random
        self._regex_generator = regex_generator

    @property
    def random(self) -> Random:
        return self._random

    def visit(self, schema: GenericSchema, **kwargs: Any) -> Any:
        if generate_method := getattr(schema, "__d42_generate__", None):
            return generate_method(self, **kwargs)
        raise NotImplementedError(f"{schema.__class__.__name__} has no method '__d42_generate__'")

    def visit_none(self, schema: NoneSchema, **kwargs: Any) -> None:
        return None

    def visit_bool(self, schema: BoolSchema, **kwargs: Any) -> bool:
        if schema.props.value is not Nil:
            return schema.props.value
        return self._random.random_choice((True, False))

    def visit_int(self, schema: IntSchema, **kwargs: Any) -> int:
        if schema.props.value is not Nil:
            return schema.props.value

        min_value = schema.props.min if (schema.props.min is not Nil) else INT_MIN
        max_value = schema.props.max if (schema.props.max is not Nil) else INT_MAX
        return self._random.random_int(min_value, max_value)

    def visit_float(self, schema: FloatSchema, **kwargs: Any) -> float:
        if schema.props.value is not Nil:
            return schema.props.value

        min_value = schema.props.min if (schema.props.min is not Nil) else FLOAT_MIN
        max_value = schema.props.max if (schema.props.max is not Nil) else FLOAT_MAX
        precision = schema.props.precision if (schema.props.precision is not Nil) else Nil

        if precision is not Nil:
            assert isinstance(precision, int)  # for type checker
            return self._random.random_float(min_value, max_value, precision)
        return self._random.random_float(min_value, max_value)

    def visit_str(self, schema: StrSchema, **kwargs: Any) -> str:
        if schema.props.value is not Nil:
            return schema.props.value

        if schema.props.pattern is not Nil:
            return self._regex_generator.generate(schema.props.pattern)

        if schema.props.len is not Nil:
            length = schema.props.len
        else:
            min_length = schema.props.min_len if (schema.props.min_len is not Nil) else STR_LEN_MIN
            max_length = schema.props.max_len if (schema.props.max_len is not Nil) else STR_LEN_MAX
            if schema.props.substr is not Nil:
                min_length = max(min_length, len(schema.props.substr))
                max_length = max(max_length, len(schema.props.substr))
            length = self._random.random_int(min_length, max_length)

        if schema.props.alphabet is not Nil:
            alphabet = schema.props.alphabet
        else:
            alphabet = STR_ALPHABET

        if schema.props.substr is not Nil:
            substr = schema.props.substr
            generated = self._random.random_str(length - len(substr), alphabet)
            offset = self._random.random_int(0, len(generated))
            return generated[0:offset] + substr + generated[offset:]

        return self._random.random_str(length, alphabet)

    def generate_unique_items(
        self,
        generate_fn: Callable[[], Any],
        target_count: int,
        require_internal_uniqueness: bool = False,
        require_strict_internal_uniqueness: bool = False,
    ) -> List[Any]:
        result: List[Any] = []
        seen: Set[str] = set()
        attempts = 0
        max_attempts = sys.getrecursionlimit()

        if target_count == 0:
            return []

        for attempts in range(1, max_attempts + 1):
            item = generate_fn()

            if not self.is_valid_unique_item(
                    item,
                    seen,
                    require_internal_uniqueness,
                    require_strict_internal_uniqueness):
                continue

            result.append(item)
            seen.add(str(item))

            if len(result) >= target_count:
                break
        else:
            msg = f"Failed to generate {target_count} unique items after {attempts} attempts"
            raise RuntimeError(msg)

        return result

    def is_valid_unique_item(self, item: Any, seen: Set[str],
                             require_internal_uniqueness: bool,
                             require_strict_internal_uniqueness: bool) -> bool:
        if require_internal_uniqueness and isinstance(item, list):
            if len(item) != len(set(str(x) for x in item)):
                return False

            if (require_strict_internal_uniqueness and item
                    and all(str(v) == str(item[0]) for v in item)):
                raise RuntimeError("Cannot generate internally unique list from identical values")

        return str(item) not in seen

    def visit_list(self, schema: ListSchema, **kwargs: Any) -> List[Any]:
        if schema.props.elements is Nil and schema.props.type is Nil:
            if (schema.props.len is Nil and schema.props.min_len is
                    Nil and schema.props.max_len is Nil):
                self._random.random_int(LIST_LEN_MIN, LIST_LEN_MAX)
                return []

            if schema.props.len is not Nil:
                length = schema.props.len
                return [[] for _ in range(length)]
            elif schema.props.min_len is not Nil or schema.props.max_len is not Nil:
                min_len = schema.props.min_len if schema.props.min_len is not Nil else LIST_LEN_MIN
                max_len = schema.props.max_len if schema.props.max_len is not Nil else LIST_LEN_MAX
                length = self._random.random_int(min_len, max_len)
                return [[] for _ in range(length)]

        if schema.props.elements is not Nil:
            elements = [e for e in schema.props.elements if not is_ellipsis(e)]
            if not elements:
                return []

            def generate_once() -> List[Any]:
                return [elem.__accept__(self, **kwargs) for elem in elements]

            if not schema.props.unique:
                return generate_once()

            all_same_schema = len(elements) >= 2 and all(
                str(elements[0]) == str(e) for e in elements)
            strict_mode = all_same_schema and schema.props.unique

            if schema.props.len is not Nil:
                return self.generate_unique_items(
                    generate_fn=generate_once,
                    target_count=schema.props.len,
                    require_internal_uniqueness=True,
                    require_strict_internal_uniqueness=strict_mode,
                )

            for _ in range(sys.getrecursionlimit()):
                candidate = generate_once()
                if len(set(map(str, candidate))) == len(candidate):
                    return candidate

            raise RuntimeError("Failed to generate a list with unique internal values")

        if schema.props.type is not Nil:
            if schema.props.len is not Nil:
                length = schema.props.len
            elif schema.props.min_len is not Nil or schema.props.max_len is not Nil:
                min_len = schema.props.min_len if schema.props.min_len is not Nil else LIST_LEN_MIN
                max_len = schema.props.max_len if schema.props.max_len is not Nil else LIST_LEN_MAX
                length = self._random.random_int(min_len, max_len)
            else:
                length = self._random.random_int(LIST_LEN_MIN, LIST_LEN_MAX)

            schema_type = schema.props.type

            def generate_fn() -> Any:
                return schema_type.__accept__(self, **kwargs)

            if schema.props.unique:
                return self.generate_unique_items(generate_fn=generate_fn, target_count=length)

            return [generate_fn() for _ in range(length)]

        return []

    def visit_dict(self, schema: DictSchema, **kwargs: Any) -> Dict[Any, Any]:
        generated: Dict[Any, Any] = {}
        if schema.props.keys is Nil:
            return generated

        for key, (val, is_optional) in schema.props.keys.items():
            if is_ellipsis(key):
                continue
            if is_optional:
                continue
            generated[key] = val.__accept__(self, **kwargs)

        return generated

    def visit_any(self, schema: AnySchema, **kwargs: Any) -> Any:
        if schema.props.types is Nil:
            return None
        chosen = self._random.random_choice(schema.props.types)
        return chosen.__accept__(self, **kwargs)

    def visit_bytes(self, schema: BytesSchema, **kwargs: Any) -> bytes:
        if schema.props.value is not Nil:
            return schema.props.value
        length = self._random.random_int(BYTES_LEN_MIN, BYTES_LEN_MAX)
        alphabet = STR_ALPHABET
        return self._random.random_str(length, alphabet).encode()

    def visit_type_alias(self, schema: GenericTypeAliasSchema[TypeAliasPropsType],
                         **kwargs: Any) -> Any:
        if schema.props.type is Nil:
            return None
        return schema.props.type.__accept__(self, **kwargs)

    def visit_datetime(self, schema: DateTimeSchema, **kwargs: Any) -> datetime:
        if schema.props.value is not Nil:
            return schema.props.value
        return datetime.utcnow()

    def visit_uuid4(self, schema: UUID4Schema, **kwargs: Any) -> UUID:
        if schema.props.value is not Nil:
            return schema.props.value
        return uuid4()

    def visit_date(self, schema: DateSchema, **kwargs: Any) -> date:
        if schema.props.value is not Nil:
            return schema.props.value
        days = self._random.random_int(-100_000, +100_000)
        return date.today() - timedelta(days=days)
