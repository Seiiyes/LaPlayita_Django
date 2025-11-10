from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def currency(value):
    if value is None:
        return "$ 0"
    return f"$ {intcomma(int(value))}"