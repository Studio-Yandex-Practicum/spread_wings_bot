import enum


class AssistanceTypes(str, enum.Enum):
    """Question types."""

    LEGAL_ASSISTANCE = "legal_assistance"
    SOCIAL_ASSISTANCE = "social_assistance"
    PSYCHOLOGICAL_ASSISTANCE = "psychological_assistance"
