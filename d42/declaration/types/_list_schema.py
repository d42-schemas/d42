import sys
from typing import Any, List, Union

from niltype import Nil, Nilable

from .._is_ellipsis import TypeOrEllipsis, is_ellipsis
from .._props import Props
from .._schema_visitor import SchemaVisitor
from .._schema_visitor import SchemaVisitorReturnType as ReturnType
from ..errors import (
    DeclarationError,
    make_already_declared_error,
    make_incorrect_len_error,
    make_incorrect_max_len_error,
    make_incorrect_min_len_error,
    make_invalid_type_error,
)
from ._schema import GenericSchema, Schema

__all__ = ("ListSchema", "ListProps",)

if sys.version_info >= (3, 10):
    from typing import TypeAlias


ElementType = TypeOrEllipsis[GenericSchema]


class ListProps(Props):
    @property
    def elements(self) -> Nilable[List[GenericSchema]]:
        return self.get("elements")

    @property
    def type(self) -> Nilable[GenericSchema]:
        return self.get("type")

    @property
    def len(self) -> Nilable[int]:
        return self.get("len")

    @property
    def min_len(self) -> Nilable[int]:
        return self.get("min_len")

    @property
    def max_len(self) -> Nilable[int]:
        return self.get("max_len")

    @property
    def unique(self) -> bool:
        value = self.get("unique")
        if value is Nil:
            return False
        return bool(value)


class ListSchema(Schema[ListProps]):
    if sys.version_info >= (3, 10):
        type: TypeAlias = List
    else:
        type: Any = List

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_list(self, **kwargs)

    def __call__(self, /,
                 elements_or_type: Union[List[ElementType], GenericSchema, Any]) -> "ListSchema":
        if not isinstance(elements_or_type, (list, Schema)):
            raise make_invalid_type_error(self, elements_or_type, (list, Schema))

        if (self.props.elements is not Nil) or (self.props.type is not Nil):
            raise make_already_declared_error(self)

        if self.props.len is not Nil:
            raise make_already_declared_error(self)
        if (self.props.min_len is not Nil) or (self.props.max_len is not Nil):
            raise make_already_declared_error(self)

        if isinstance(elements_or_type, Schema):
            return self.__class__(self.props.update(type=elements_or_type))

        for index, element in enumerate(elements_or_type):
            if not isinstance(element, (Schema, type(...))):
                raise make_invalid_type_error(self, element, (Schema, type(...)))
            if is_ellipsis(element):
                if (index != 0) and (index != len(elements_or_type) - 1):
                    raise DeclarationError("`...` must be first or last element")

        if len(elements_or_type) == 2 and \
           is_ellipsis(elements_or_type[0]) and is_ellipsis(elements_or_type[-1]):
            raise DeclarationError("`...` must be first or last element")

        return self.__class__(self.props.update(elements=elements_or_type))

    def __declare_len(self, props: ListProps, length: Any) -> ListProps:
        if not isinstance(length, int):
            raise make_invalid_type_error(self, length, (int,))

        if props.elements is not Nil:
            concrete_elements = [x for x in props.elements if not is_ellipsis(x)]
            if len(props.elements) == len(concrete_elements):
                if length != len(concrete_elements):
                    raise make_incorrect_len_error(self, concrete_elements, length)
            else:
                if length < len(concrete_elements):
                    raise make_incorrect_min_len_error(self, concrete_elements, length)

        return props.update(len=length)

    def __declare_min_len(self, props: ListProps, min_length: Any) -> ListProps:
        if not isinstance(min_length, int):
            raise make_invalid_type_error(self, min_length, (int,))

        if props.elements is not Nil:
            concrete_elements = [x for x in props.elements if not is_ellipsis(x)]
            if min_length > len(concrete_elements):
                raise make_incorrect_min_len_error(self, concrete_elements, min_length)

        return props.update(min_len=min_length)

    def __declare_max_len(self, props: ListProps, max_length: Any) -> ListProps:
        if not isinstance(max_length, int):
            raise make_invalid_type_error(self, max_length, (int,))

        if props.elements is not Nil:
            concrete_elements = [x for x in props.elements if not is_ellipsis(x)]
            if max_length < len(concrete_elements):
                raise make_incorrect_max_len_error(self, concrete_elements, max_length)

        return props.update(max_len=max_length)

    def len(self, /, val_or_min: TypeOrEllipsis[int],
            max: Nilable[TypeOrEllipsis[int]] = Nil) -> "ListSchema":
        if self.props.len is not Nil:
            raise make_already_declared_error(self)

        if (self.props.min_len is not Nil) or (self.props.max_len is not Nil):
            raise make_already_declared_error(self)

        props = self.props
        if is_ellipsis(val_or_min):
            props = self.__declare_max_len(props, max)
        else:
            if max is Nil:
                props = self.__declare_len(props, val_or_min)
            elif is_ellipsis(max):
                props = self.__declare_min_len(props, val_or_min)
            else:
                props = self.__declare_max_len(self.__declare_min_len(props, val_or_min), max)
        return self.__class__(props)

    def unique(self) -> "ListSchema":
        if self.props.unique:
            raise make_already_declared_error(self)
        props = self.props.update(unique=True)
        return self.__class__(props)
