from typing import Any, Awaitable, Callable

from bot.constants.states.ask_question_states import AskQuestionStates
from bot.constants.states.main_states import States
from bot.handlers.ask_question import (
    get_question,
    get_name,
    select_contact_type,
    get_contact,
    back,
    ask_cancel
)
from bot.handlers.assistance import (
    contact_with_us,
    receive_assistance,
    select_type_of_help,
    selected_type_assistance,
    show_contact,
    ask_question
)
from bot.handlers.main_handlers import start

FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[States]]] = {
    States.SHOW_CONTACT: show_contact,
    States.CONTACT_US: contact_with_us,
    States.QUESTIONS_AND_CONTACTS: selected_type_assistance,
    States.ASSISTANCE_TYPE: select_type_of_help,
    States.REGION: receive_assistance,
    States.ASSISTANCE.value: start,
    States.ASK_QUESTION.value: ask_question,
}

ASK_FUNCTIONS: dict[str, Callable[[Any, Any], Awaitable[AskQuestionStates]]] = {
    AskQuestionStates.QUESTION: get_question,
    AskQuestionStates.NAME: get_name,
    AskQuestionStates.CONTACT_TYPE: select_contact_type,
    AskQuestionStates.ENTER_YOUR_CONTACT: get_contact,
    AskQuestionStates.BACK: back,
    AskQuestionStates.CANCEL: ask_cancel
}