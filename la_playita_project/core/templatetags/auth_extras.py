from django import template

register = template.Library()

@register.filter(name='has_role')
def has_role(user, role_name):
    """Template filter to check if a user has a specific role."""
    if user.rol:
        return user.rol.nombre == role_name
    return False