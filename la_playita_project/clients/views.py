from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import check_user_role
from .models import Cliente


@login_required
@check_user_role(allowed_roles=['Administrador'])
def cliente_list(request):
    """
    Vista para listar todos los clientes.
    """
    clientes = Cliente.objects.all().order_by('nombres')
    return render(request, 'clients/cliente_list.html', {'clientes': clientes})