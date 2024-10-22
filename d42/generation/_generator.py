from datetime import date, datetime, timedelta
from typing import Any, Dict, List
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
        if schema.props.inner_schema is not Nil:
            import json
            serialize = json.dumps
            return serialize(schema.props.inner_schema.__accept__(self, **kwargs), default=str)

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

    def visit_list(self, schema: ListSchema, **kwargs: Any) -> List[Any]:
        if schema.props.elements is not Nil:
            elements = []
            for elem in schema.props.elements:
                if is_ellipsis(elem):
                    continue
                elements.append(elem.__accept__(self, **kwargs))
            return elements

        is_length_specified = False
        if schema.props.len is not Nil:
            length = schema.props.len
            is_length_specified = True
        else:
            min_length = LIST_LEN_MIN
            if schema.props.min_len is not Nil:
                min_length = schema.props.min_len
                is_length_specified = True
            max_length = LIST_LEN_MAX
            if schema.props.max_len is not Nil:
                max_length = schema.props.max_len
                is_length_specified = True
            length = self._random.random_int(min_length, max_length)

        if schema.props.type is not Nil:
            return [schema.props.type.__accept__(self, **kwargs) for _ in range(length)]

        if is_length_specified:
            return [[] for _ in range(length)]
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
