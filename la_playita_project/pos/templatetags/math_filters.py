from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    """
    Multiplica el valor por el argumento.
    Uso: {{ value|mul:2 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """
    Divide el valor por el argumento.
    Uso: {{ value|div:2 }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def sub(value, arg):
    """
    Resta el argumento del valor.
    Uso: {{ value|sub:10 }}
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
