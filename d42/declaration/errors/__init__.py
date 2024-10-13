from typing import TYPE_CHECKING, Any, Sized, Tuple, Type

if TYPE_CHECKING:
    from ..types import GenericSchema

__all__ = ("DeclarationError", "make_invalid_type_error", "make_already_declared_error",
           "make_incorrect_len_error", "make_incorrect_min_error", "make_incorrect_max_error",
           "make_incorrect_min_len_error", "make_incorrect_max_len_error",
           "make_incorrect_precision_error",)


class DeclarationError(Exception):
    pass


def _get_type_name(type_: Type[Any]) -> str:
    return str(getattr(type_, "__name__", type_))


def make_invalid_type_error(schema: "GenericSchema", value: Any,
                            types: Tuple[Type[Any], ...]) -> DeclarationError:
    value_type = type(value)
    value_type_name = _get_type_name(value_type)

    types_ = tuple(map(_get_type_name, types))
    if len(types) == 1:
        message = (f"`{schema!r}` value must be an instance of '{_get_type_name(types[0])}', "
                   f"instance of {value_type_name!r} {value!r} given")
    else:
        message = (f"`{schema!r}` value must be an instance of {types_!r}, "
                   f"instance of {value_type_name!r} given")
    return DeclarationError(message)


def make_already_declared_error(schema: "GenericSchema") -> DeclarationError:
    message = f"`{schema!r}` is already declared"
    return DeclarationError(message)


def make_incorrect_min_error(schema: "GenericSchema",
                             value: Any, min_value: Any) -> DeclarationError:
    message = f"`{schema!r}` min value must be less than or equal to {value}, {min_value} given"
    return DeclarationError(message)


def make_incorrect_max_error(schema: "GenericSchema",
                             value: Any, max_value: Any) -> DeclarationError:
    message = f"`{schema!r}` max value must be greater than or equal to {value}, {max_value} given"
    return DeclarationError(message)


def make_incorrect_len_error(schema: "GenericSchema",
                             value: Sized, length: int) -> DeclarationError:
    message = f"`{schema!r}` len must be equal to {len(value)}, {length} given"
    return DeclarationError(message)


def make_incorrect_min_len_error(schema: "GenericSchema",
                                 value: Sized, min_length: int) -> DeclarationError:
    message = (f"`{schema!r}` min len must be less than or equal to {len(value)}, "
               f"{min_length} given")
    return DeclarationError(message)


def make_incorrect_max_len_error(schema: "GenericSchema",
                                 value: Sized, max_length: int) -> DeclarationError:
    message = (f"`{schema!r}` max len must be greater than or equal to {len(value)}, "
               f"{max_length} given")
    return DeclarationError(message)


def make_incorrect_precision_error(schema: "GenericSchema",
                                   precision: int, max_precision: int) -> DeclarationError:
    message = (f"`{schema!r}` precision must be greater than 0 or less than {max_precision}, "
               f"{precision} given")
    return DeclarationError(message)
