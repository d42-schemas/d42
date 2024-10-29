import sys
from typing import Any, Generator, List, Tuple

from niltype import Nil, Nilable

from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import make_already_declared_error, make_invalid_type_error
from ._schema import GenericSchema, Schema

__all__ = ("AnySchema", "AnyProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


class AnyProps(Props):
    """
    Represents the properties specific to `AnySchema`.
    """

    @property
    def types(self) -> Nilable[Tuple[GenericSchema, ...]]:
        """
        Retrieve the types associated with the `AnySchema`.

        :return: A tuple of `GenericSchema` instances if types are set; otherwise, `Nil`.
        """
        return self.get("types")


class AnySchema(Schema[AnyProps]):
    """
    Represents a schema that can match any of a given set of sub-schemas.
    """

    if sys.version_info >= (3, 10):
        type: TypeAlias = Any
    else:
        type: Any = Any

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        """
        Accept a visitor to perform operations on this schema.

        This method is used in the visitor pattern, allowing external classes
        to define operations on the schema without modifying its class.

        :param visitor: The visitor instance that defines operations for this schema.
        :param kwargs: Additional arguments to pass to the visitor's `visit_any` method.
        :return: The result of the visitor's `visit_any` method.
        """
        return visitor.visit_any(self, **kwargs)

    def __call__(self, /, type_: GenericSchema, *types: GenericSchema) -> "AnySchema":
        """
        Define the set of schemas that `AnySchema` should contain.

        Accepts one or more `GenericSchema` instances and validates that each one
        is an instance of `Schema`. If types are already declared, raises an error.
        Also flattens any nested `AnySchema` instances for easier access.

        :param type_: The first `GenericSchema` instance to include.
        :param types: Additional `GenericSchema` instances to include.
        :return: A new `AnySchema` instance with the specified types.
        :raises DeclarationError: If any provided schema is not an instance of `Schema`,
                                  or if types have already been declared for this schema.
        """
        types_ = (type_,) + types
        for t in types_:
            if not isinstance(t, Schema):
                raise make_invalid_type_error(self, t, (Schema,))

        if self.props.types is not Nil:
            raise make_already_declared_error(self)

        flattened_types = self._flatten_schemas(types_)
        return self.__class__(self.props.update(types=flattened_types))

    def _flatten_schemas(self, schemas: Tuple[GenericSchema, ...]) -> Tuple[GenericSchema, ...]:
        """
        Recursively flatten nested `AnySchema` instances within the provided schemas.

        If an `AnySchema` instance with defined types is encountered within the provided
        schemas, its types are extracted and flattened into a single list.

        :param schemas: A tuple of `GenericSchema` instances to flatten.
        :return: A tuple of flattened `GenericSchema` instances.
        """
        flattened: List[GenericSchema] = []

        for schema in schemas:
            if isinstance(schema, AnySchema) and (schema.props.types is not Nil):
                # Recursively flatten nested AnySchema instances
                flattened.extend(self._flatten_schemas(schema.props.types))
            else:
                flattened.append(schema)

        return tuple(flattened)

    def __iter__(self) -> Generator[GenericSchema, None, None]:
        """
        Yield each schema in `types` if they are defined, otherwise yield an empty sequence.

        This allows `AnySchema` to be iterable, providing access to each schema
        it contains if types have been set.

        :return: A generator that yields `GenericSchema` instances from `types`.
        """
        if self.props.types is not Nil:
            yield from self.props.types
        else:
            yield from ()
