import re


def to_snake_case(text: str) -> str:
    """Convert text to snake case."""
    text = re.sub(r'[\W_]+', ' ', text)
    return '_'.join(text.lower().split())
