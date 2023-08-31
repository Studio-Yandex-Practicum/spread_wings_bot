from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Add class filter."""
    return field.as_widget(attrs={"class": css})


@register.filter
def addid(field, css):
    """Add id filter."""
    return field.as_widget(attrs={"id": css})
