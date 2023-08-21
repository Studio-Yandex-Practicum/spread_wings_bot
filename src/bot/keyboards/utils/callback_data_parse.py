import re
from typing import Optional, Tuple, Union


def parse_callback_data(
    callback_data: str, pattern: str
) -> Union[Tuple[Optional[str], Optional[int]], int]:
    """Parse data to get page number and bot state for pagination."""
    match = re.match(pattern, callback_data)
    if not match:
        return None, None
    bot_state, number = match.groups()
    number = int(number) if number is not None else None
    return bot_state, number
