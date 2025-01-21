from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return value - arg
    except (TypeError, ValueError):
        return 0
