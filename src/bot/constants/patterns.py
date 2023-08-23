from bot.constants.states import States
from bot.models import HelpTypes

PAGE_SEP_SYMBOL = "#"
PATTERN = "^{state}$"

MESSAGE_PATTERN = r"^[^\/].*$"
BACK = r"back_to_"
CONTACT = PATTERN.format(state="EMAIL|PHONE|TELEGRAM")
POSSIBLE_TYPE_OF_ASSISTANCE = PATTERN.format(
    state="".join(f"{h_type}|" for h_type in HelpTypes.names)
)
HELP_TYPE = rf"({POSSIBLE_TYPE_OF_ASSISTANCE})(?:{PAGE_SEP_SYMBOL}(\d+))?"
CONTACT_TYPE = PATTERN.format(state=States.CONTACT_TYPE.value)
GET_USER_QUESTION = PATTERN.format(state=States.GET_USER_QUESTION.value)
GET_ASSISTANCE = PATTERN.format(state=States.GET_ASSISTANCE.value)
FUND_PROGRAMS = PATTERN.format(
    state=rf"({States.FUND_PROGRAMS.value})(?:{PAGE_SEP_SYMBOL}(\d+))?"
)
SHOW_PROGRAM = rf"({States.SHOW_PROGRAM.value})(?:{PAGE_SEP_SYMBOL}(\d+))?"
CONTACT_US = PATTERN.format(state=States.CONTACT_US.value)
SHOW_CONTACT = PATTERN.format(state=States.SHOW_CONTACT.value)
USERNAME_AFTER_RETURNING = (
    PATTERN.format(state=States.USERNAME_AFTER_RETURNING.value),
)
GET_USERNAME = PATTERN.format(state=States.GET_USERNAME.value)
