from bot.constants.states import States
from bot.handlers.assistance import receive_assistance
from bot.handlers.main_handlers import start

FUNCTIONS = {
    States.REGION.value: receive_assistance,
    States.ASSISTANCE.value: start,
}
