class InvalidRecipientEmailAddress(Exception):
    """Custom extraction for lifting with an invalid addressee."""

    pass


class PostNotFound(Exception):
    """Custom exeption for lifting in the absence of a moking post."""

    pass
