from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return value - arg
    except (TypeError, ValueError):
        return 0

@register.filter
def stars(value):
    return "★" * int(value)

@register.filter
def average_star(value, args):
    try:
        # Ensure both value and args are converted to float
        value = float(value)
        args = float(args)

        # Avoid division by zero
        if args == 0:
            return ""

        # Calculate average
        average = value / args
        return "★" * int(average)  # Display stars based on the average
    except (ValueError, ZeroDivisionError):
        return ""  # Return empty string if there's an error
