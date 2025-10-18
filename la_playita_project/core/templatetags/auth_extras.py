from django import template
from datetime import date

register = template.Library()

@register.filter(name='has_role')
def has_role(user, role_name):
    """Template filter to check if a user has a specific role."""
    if user.rol:
        return user.rol.nombre == role_name
    return False

@register.filter(name='days_until')
def days_until(value):
    """
    Calculates the number of days between the given date and today.
    Returns None if the value is not a date object.
    """
    if not isinstance(value, date):
        return None
    today = date.today()
    delta = value - today
    return delta.days