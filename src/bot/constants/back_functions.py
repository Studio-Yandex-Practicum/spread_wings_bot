from bot.constants.states import States
from bot.handlers.assistance import receive_assistance
from bot.handlers.assistance_types import select_type_of_help
from bot.handlers.main_handlers import start

FUNCTIONS = {
    States.REGION.value: receive_assistance,
    States.ASSISTANCE.value: start,
    States.ASSISTANCE_TYPE: select_type_of_help,
}
