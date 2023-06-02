from typing import Any, Awaitable, Callable

from bot.constants.states import States
from bot.handlers.assistance import receive_assistance
from bot.handlers.main_handlers import start

FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.REGION.value: receive_assistance,
    States.ASSISTANCE.value: start,
}
