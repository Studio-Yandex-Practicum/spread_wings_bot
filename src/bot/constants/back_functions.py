from typing import Any, Awaitable, Callable

from bot.constants.states.main_states import States
from bot.handlers.assistance import (
    contact_with_us,
    receive_assistance,
    select_type_of_help,
    selected_type_assistance,
    show_contact,
)
from bot.handlers.main_handlers import start

FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.SELECTED_TYPE: selected_type_assistance,
    States.REGION.value: receive_assistance,
    States.SHOW_CONTACT: show_contact,
    States.CONTACT_US: contact_with_us,
    States.QUESTIONS_AND_CONTACTS: selected_type_assistance,
    States.ASSISTANCE_TYPE: select_type_of_help,
    States.REGION: receive_assistance,
    States.ASSISTANCE.value: start,
}
