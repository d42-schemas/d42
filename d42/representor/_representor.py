from typing import Any, cast

from niltype import Nil

from d42.declaration import SchemaVisitor, is_ellipsis
from d42.declaration.types import (
    AnySchema,
    BoolSchema,
    BytesSchema,
    DateSchema,
    DateTimeSchema,
    DictSchema,
    FloatSchema,
    GenericSchema,
    GenericTypeAliasSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    TypeAliasPropsType,
    UUID4Schema,
)


class Representor(SchemaVisitor[str]):
    def __init__(self, name: str = "schema", indent: int = 4) -> None:
        self._name = name
        self._indent = indent

    @property
    def name(self) -> str:
        return self._name

    def visit(self, schema: GenericSchema, *, indent: int = 0, **kwargs: Any) -> str:
        if represent_method := getattr(schema, "__district42__", None):
            return cast(str, represent_method(self, indent=indent, **kwargs))
        raise NotImplementedError(f"{schema.__class__.__name__} has no method '__district42__'")

    def visit_none(self, schema: NoneSchema, *, indent: int = 0, **kwargs: Any) -> str:
        return f"{self._name}.none"

    def visit_bool(self, schema: BoolSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.bool"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"
        return r

    def visit_int(self, schema: IntSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.int"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        if schema.props.min is not Nil:
            r += f".min({schema.props.min!r})"

        if schema.props.max is not Nil:
            r += f".max({schema.props.max!r})"

        return r

    def visit_float(self, schema: FloatSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.float"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        if schema.props.min is not Nil:
            r += f".min({schema.props.min!r})"

        if schema.props.max is not Nil:
            r += f".max({schema.props.max!r})"

        if schema.props.precision is not Nil:
            r += f".precision({schema.props.precision!r})"

        return r

    def visit_str(self, schema: StrSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.str"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        if schema.props.alphabet is not Nil:
            r += f".alphabet({schema.props.alphabet!r})"

        if schema.props.substr is not Nil:
            r += f".contains({schema.props.substr!r})"

        if schema.props.pattern is not Nil:
            r += f".regex({schema.props.pattern!r})"

        if schema.props.len is not Nil:
            r += f".len({schema.props.len!r})"
        elif (schema.props.min_len is not Nil) and (schema.props.max_len is not Nil):
            r += f".len({schema.props.min_len!r}, {schema.props.max_len!r})"
        elif schema.props.min_len is not Nil:
            r += f".len({schema.props.min_len!r}, ...)"
        elif schema.props.max_len is not Nil:
            r += f".len(..., {schema.props.max_len!r})"

        return r

    def visit_list(self, schema: ListSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.list"

        if schema.props.type is not Nil:
            r += "({})".format(schema.props.type.__accept__(self, indent=indent, **kwargs))
        elif schema.props.elements is not Nil:
            if len(schema.props.elements) == 0:
                return r + "([])"
            elems = []
            for element in schema.props.elements:
                if is_ellipsis(element):
                    elem = "..."
                else:
                    elem = element.__accept__(self, indent=indent + self._indent, **kwargs)
                elems.append(" " * (indent + self._indent) + elem)
            r += "([\n"
            r += ",\n".join(elems)
            r += "\n" + " " * indent + "])"

        if schema.props.len is not Nil:
            r += f".len({schema.props.len!r})"
        elif (schema.props.min_len is not Nil) and (schema.props.max_len is not Nil):
            r += f".len({schema.props.min_len!r}, {schema.props.max_len!r})"
        elif schema.props.min_len is not Nil:
            r += f".len({schema.props.min_len!r}, ...)"
        elif schema.props.max_len is not Nil:
            r += f".len(..., {schema.props.max_len!r})"

        return r

    def visit_dict(self, schema: DictSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.dict"

        if schema.props.keys is Nil:
            return r

        if len(schema.props.keys) == 0:
            return r + "({})"
        elif (len(schema.props.keys) == 1) and (... in schema.props.keys):
            return r + "({...: ...})"

        pairs = []
        for key, (val, is_optional) in schema.props.keys.items():
            if is_ellipsis(key):
                key_repr = val_repr = "..."
            else:
                key_repr = f"optional({key!r})" if is_optional else repr(key)
                val_repr = val.__accept__(self, indent=indent + self._indent, **kwargs)
            pairs.append("{indent}{key}: {val}".format(
                indent=" " * (indent + self._indent),
                key=key_repr,
                val=val_repr,
            ))

        r += "({\n"
        r += ",\n".join(pairs) + "\n"
        r += " " * indent + "})"

        return r

    def visit_any(self, schema: AnySchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.any"

        if schema.props.types is not Nil:
            types = [x.__accept__(self, indent=indent, **kwargs) for x in schema.props.types]
            r += "({})".format(", ".join(types))
        return r

    def visit_bytes(self, schema: BytesSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.bytes"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"
        return r

    def visit_type_alias(self, schema: GenericTypeAliasSchema[TypeAliasPropsType],
                         *, indent: int = 0, **kwargs: Any) -> str:
        type_name = schema.__class__.__name__
        type_repr = schema.props.type.__accept__(self, indent=indent, **kwargs)
        if schema.props.name is not Nil:
            type_name = schema.props.name
        return f"{type_name}<{type_repr}>"

    def visit_uuid4(self, schema: UUID4Schema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.uuid4"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        return r

    def visit_datetime(self, schema: DateTimeSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.datetime"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        return r

    def visit_date(self, schema: DateSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.date"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        return r
