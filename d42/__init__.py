import blahblah
import district42
import revolt  # noqa: F401
import valera

try:
    make_required = district42.make_required
except AttributeError:
    from typing import Any

    def make_required(schema: Any, keys: Any = None) -> Any:
        raise ValueError("make_required is not available in district42 < 1.8.0")

schema = district42.schema
optional = district42.optional
from_native = district42.from_native
register_type = district42.register_type

fake = blahblah.fake

validate = valera.validate
validate_or_fail = valera.validate_or_fail
ValidationException = valera.ValidationException

substitute = revolt.substitute

__all__ = (
    "schema", "optional", "from_native", "register_type", "make_required",
    "fake",
    "validate", "validate_or_fail", "ValidationException",
    "substitute",
)
__version__ = "1.8.0"

# utils/rollout
