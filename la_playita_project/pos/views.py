from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import check_user_role


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pos_view(request):
    """
    Vista principal del Punto de Venta (POS).
    """
    return render(request, 'pos/pos_main.html')