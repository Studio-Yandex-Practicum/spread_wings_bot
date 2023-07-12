__all__ = [
    "generate_dict_factory",
    "START_COMMON_TEMPLATE",
    "MAIN_COORDINATORS_TEMPLATE",
    "END_COMMON_TEMPLATE",
]
from .service import generate_dict_factory
from .templates import (
    END_COMMON_TEMPLATE,
    MAIN_COORDINATORS_TEMPLATE,
    START_COMMON_TEMPLATE,
)
