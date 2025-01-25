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
    try:
        value = float(value)
        full_stars = int(value)
        half_star = 1 if value % 1 >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        return "★" * full_stars + "☆" * half_star + "☆" * empty_stars
    except (ValueError, TypeError):
        return ""

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
