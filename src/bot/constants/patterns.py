from bot.constants.states import States
from bot.models import HelpTypes

PAGE_SEP_SYMBOL = "#"
PATTERN = "^{state}$"

MESSAGE_PATTERN = r"^[^\/].*$"
BACK = r"back_to_"
CONTACT = PATTERN.format(state="EMAIL|PHONE|TELEGRAM")
HELP_TYPE = PATTERN.format(
    state="".join(f"{h_type}|" for h_type in HelpTypes.names)
)
PARSE_CALLBACK_DATA = rf"({HELP_TYPE})(?:{PAGE_SEP_SYMBOL}(\d+))?"
CONTACT_TYPE = PATTERN.format(state=States.CONTACT_TYPE.value)
ASK_QUESTION = PATTERN.format(state=States.ASK_QUESTION.value)
ASSISTANCE = PATTERN.format(state=States.ASSISTANCE.value)
FUND_PROGRAMS = PATTERN.format(state=States.FUND_PROGRAMS.value)
CONTACT_US = PATTERN.format(state=States.CONTACT_US.value)
SHOW_CONTACT = PATTERN.format(state=States.SHOW_CONTACT.value)
NAME = (PATTERN.format(state=States.NAME.value),)
QUESTION = PATTERN.format(state=States.QUESTION.value)
