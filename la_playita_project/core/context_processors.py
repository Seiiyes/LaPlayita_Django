def role_flags(request):
    """Inyecta banderas de rol en el contexto de las plantillas.

    Añade `user_is_admin` y `user_is_vendedor` para simplificar las plantillas
    y centralizar la lógica de comprobación de roles.
    """
    user = getattr(request, 'user', None)
    is_admin = False
    is_vendedor = False
    try:
        if user and getattr(user, 'is_authenticated', False):
            rol = getattr(user, 'rol', None)
            nombre = getattr(rol, 'nombre', None) if rol else None
            is_admin = nombre == 'Administrador'
            is_vendedor = nombre == 'Vendedor'
    except Exception:
        # En caso de cualquier problema, devolver False por seguridad
        is_admin = False
        is_vendedor = False

    return {
        'user_is_admin': is_admin,
        'user_is_vendedor': is_vendedor,
    }
