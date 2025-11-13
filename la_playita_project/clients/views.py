from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import check_user_role
from .models import Cliente
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
@check_user_role(allowed_roles=['Administrador'])
def cliente_list(request):
    """
    Vista para listar todos los clientes.
    """
    clientes = Cliente.objects.all().order_by('nombres')
    return render(request, 'clients/cliente_list.html', {'clientes': clientes})

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def cliente_create_ajax(request):
    try:
        data = json.loads(request.body)
        # Validar que el documento no exista
        if Cliente.objects.filter(documento=data.get('documento')).exists():
            return JsonResponse({'error': 'Ya existe un cliente con este documento.'}, status=400)
            
        cliente = Cliente.objects.create(
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            documento=data.get('documento'),
            telefono=data.get('telefono'),
            email=data.get('email'),
        )
        return JsonResponse({
            'id': cliente.id,
            'nombres': cliente.nombres,
            'apellidos': cliente.apellidos,
            'documento': cliente.documento,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)