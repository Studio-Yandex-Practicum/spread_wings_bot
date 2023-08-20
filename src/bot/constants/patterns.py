from bot.constants.states import States
from bot.models import HelpTypes

BACK = r"back_to_"
PAGE_SEP_SYMBOL = "#"
PATTERN = "^{state}$"
MESSAGE_PATTERN = r"^[^\/].*$"
POSSIBLE_TYPE_OF_ASSISTANCE = PATTERN.format(
    state="".join(f"{h_type}|" for h_type in HelpTypes.names)
)

CONTACT_TYPE = PATTERN.format(state="EMAIL|PHONE|TELEGRAM")
CONTACT_US = PATTERN.format(state=States.CONTACT_US.value)
GET_ASSISTANCE = PATTERN.format(state=States.GET_ASSISTANCE.value)
GET_CONTACT_TYPE = PATTERN.format(state=States.GET_CONTACT_TYPE.value)
GET_USERNAME = PATTERN.format(state=States.GET_USERNAME.value)
GET_USER_QUESTION = PATTERN.format(state=States.GET_USER_QUESTION.value)
FUND_PROGRAMS = PATTERN.format(
    state=rf"({States.FUND_PROGRAMS.value})(?:{PAGE_SEP_SYMBOL}(\d+))?"
)
HELP_TYPE = rf"({POSSIBLE_TYPE_OF_ASSISTANCE})(?:{PAGE_SEP_SYMBOL}(\d+))?"
PARSE_FUND_PROGRAMS_CALLBACK_DATA = (
    rf"({States.FUND_PROGRAMS.value}:{PAGE_SEP_SYMBOL}(\d+))?"
)
SHOW_CONTACT = PATTERN.format(state=States.SHOW_CONTACT.value)
