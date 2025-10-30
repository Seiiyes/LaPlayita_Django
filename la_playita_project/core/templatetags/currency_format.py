import locale
from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value):
    """
    Formats a number as a currency string.
    """
    try:
        # Attempt to set the locale to Spanish (Colombia)
        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
        except locale.Error:
            # Fallback for systems without Spanish language pack
            pass
        
        # Convert the value to a float before formatting
        return locale.currency(float(value), grouping=True)
    except (ValueError, TypeError):
        return None
