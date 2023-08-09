from bot.constants.states.main_states import States

PATTERN = "^{state}$"

MESSAGE_PATTERN = r"^[^\/].*$"
BACK = r"back_to_"
CONTACT = PATTERN.format(state="EMAIL|PHONE|TELEGRAM")
HELP_TYPE = PATTERN.format(
    state="LEGAL_ASSISTANCE|SOCIAL_ASSISTANCE|" "PSYCHOLOGICAL_ASSISTANCE"
)
CONTACT_TYPE = PATTERN.format(state=States.CONTACT_TYPE.value)
ASK_QUESTION = PATTERN.format(state=States.ASK_QUESTION.value)
ASSISTANCE = PATTERN.format(state=States.ASSISTANCE.value)
FUND_PROGRAMS = PATTERN.format(state=States.FUND_PROGRAMS.value)
CONTACT_US = PATTERN.format(state=States.CONTACT_US.value)
SHOW_CONTACT = PATTERN.format(state=States.SHOW_CONTACT.value)
