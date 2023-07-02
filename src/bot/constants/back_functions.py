from typing import Any, Awaitable, Callable

from bot.constants.states.main_states import States
from bot.handlers.assistance import receive_assistance
from bot.handlers.assistance_types import contact_with_us, select_type_of_help
from bot.handlers.main_handlers import start

FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.REGION.value: receive_assistance,
    States.ASSISTANCE.value: start,
    States.ASSISTANCE_TYPE: select_type_of_help,
    States.CONTACT_US: contact_with_us,
    States.HOME: start,
}
