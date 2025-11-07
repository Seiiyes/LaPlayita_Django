from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    """Template filter to subtract two numbers."""
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except (ValueError, TypeError, InvalidOperation):
        return 0

@register.filter(name='multiply')
def multiply(value, arg):
    """Template filter to multiply two numbers."""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError, InvalidOperation):
        return 0