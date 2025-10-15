from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def check_user_role(allowed_roles=[]):
    """
    Decorador para verificar si el rol_id de un usuario está en una lista de roles permitidos.
    Redirige si el usuario no está autenticado o no tiene el rol requerido.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para acceder a esta página.")
                return redirect('auth_login')

            if request.user.rol_id not in allowed_roles:
                messages.error(request, "No tienes los permisos necesarios para ver esta página.")
                # Redirige al dashboard o a una página principal si no tienen permiso.
                return redirect('dashboard') 

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# El código anterior se puede mantener por si se usa en otro lugar o para referencia.
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

# Mapeo de ROL ID a nombres legibles
ROL_MAP = {
    1: 'Admin',
    2: 'Vendedor',
}

def user_has_role_id(user, required_role_names):
    """Verifica si el rol_id del usuario coincide con los nombres de roles requeridos."""
    if not user.is_authenticated:
        return False
        
    user_role_name = ROL_MAP.get(user.rol_id)
    return user_role_name in required_role_names

def group_required(*required_roles):
    """Decorador que requiere que el usuario tenga uno de los roles (por nombre) basado en rol_id."""
    def check_roles(user):
        return user_has_role_id(user, required_roles)
        
    # Redirige a 'auth:login' si falla el permiso
    return user_passes_test(check_roles, login_url=reverse_lazy('auth:login'))
