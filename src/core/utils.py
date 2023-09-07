import re

HTML_NEW_PARAGRAPH_SYMBOL = "<br />"
TELEGRAM_NEW_PARAGRAPH_SYMBOL = " "


def to_snake_case(text: str) -> str:
    """Convert text to snake case."""
    text = re.sub(r"[\W_]+", " ", text)
    return "_".join(text.lower().split())


def convert_br_tags_to_telegram_message(message):
    """Convert <br> tags from HTML to whitespace for telegram message."""
    return message.replace(
        HTML_NEW_PARAGRAPH_SYMBOL, TELEGRAM_NEW_PARAGRAPH_SYMBOL
    )
