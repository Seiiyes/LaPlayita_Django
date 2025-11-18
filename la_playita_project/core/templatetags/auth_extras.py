from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_role')
def has_role(user, role_name):
    """
    Verifica si el rol del usuario coincide con el nombre del rol proporcionado.
    Usa la relación `rol` del modelo de usuario personalizado.
    """
    if not hasattr(user, 'rol') or not user.rol:
        return False
    return user.rol.nombre == role_name