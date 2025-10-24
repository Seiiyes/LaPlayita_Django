from django import template
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='currency')
def currency(value):
    """
    Formatea un número como moneda COP: $670,000
    """
    if value is None:
        return '$0'
    
    # Convertir a entero y luego a string
    try:
        num = int(float(value))
        num_str = str(num)
    except (ValueError, TypeError):
        return '$0'
    
    # Formatear con separadores de miles manualmente
    result = []
    for i, digit in enumerate(reversed(num_str)):
        if i > 0 and i % 3 == 0:
            result.append(',')
        result.append(digit)
    return f'${("".join(reversed(result)))}'