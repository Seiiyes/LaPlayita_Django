from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import check_user_role
from .models import Cliente, PuntosFidelizacion, ProductoCanjeble, CanjeProducto
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal

@login_required
@check_user_role(allowed_roles=['Administrador'])
def cliente_list(request):
    """Vista para listar todos los clientes."""
    clientes = Cliente.objects.all().order_by('nombres')
    return render(request, 'clients/cliente_list.html', {'clientes': clientes})

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def cliente_create_ajax(request):
    """Crear cliente vía AJAX"""
    try:
        data = json.loads(request.body)
        if Cliente.objects.filter(documento=data.get('documento')).exists():
            return JsonResponse({'error': 'Ya existe un cliente con este documento.'}, status=400)
        cliente = Cliente.objects.create(
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            documento=data.get('documento'),
            telefono=data.get('telefono'),
            correo=data.get('email'),
        )
        return JsonResponse({
            'id': cliente.id,
            'nombres': cliente.nombres,
            'apellidos': cliente.apellidos,
            'documento': cliente.documento,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def panel_puntos(request, cliente_id):
    """Panel de puntos del cliente - Ver saldo y transacciones"""
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    transacciones = PuntosFidelizacion.objects.filter(cliente_id=cliente_id).order_by('-fecha_transaccion')[:20]
    
    context = {
        'cliente': cliente,
        'transacciones': transacciones,
        'puntos_totales': cliente.puntos_totales,
    }
    return render(request, 'clients/panel_puntos.html', context)

@login_required
def historial_puntos(request, cliente_id):
    """Historial completo de puntos del cliente"""
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    transacciones = PuntosFidelizacion.objects.filter(cliente_id=cliente_id).order_by('-fecha_transaccion')
    
    context = {
        'cliente': cliente,
        'transacciones': transacciones,
    }
    return render(request, 'clients/historial_puntos.html', context)

@login_required
def productos_canjebles(request):
    """Lista de productos canjeables"""
    productos = ProductoCanjeble.objects.filter(activo=True, stock_disponible__gt=0).order_by('puntos_requeridos')
    
    context = {
        'productos': productos,
    }
    return render(request, 'clients/productos_canjebles.html', context)

@login_required
def mi_panel_puntos(request):
    """Panel de puntos personal (cliente logueado)"""
    cliente = Cliente.objects.filter(correo=request.user.email).first()
    
    if not cliente:
        return render(request, 'clients/sin_cliente.html', {
            'mensaje': 'No tienes perfil de cliente asociado'
        })
    
    transacciones = PuntosFidelizacion.objects.filter(cliente_id=cliente.id).order_by('-fecha_transaccion')[:10]
    canjes = CanjeProducto.objects.filter(cliente_id=cliente.id).order_by('-fecha_canje')[:5]
    productos = ProductoCanjeble.objects.filter(activo=True, stock_disponible__gt=0).order_by('puntos_requeridos')
    
    context = {
        'cliente': cliente,
        'transacciones': transacciones,
        'canjes': canjes,
        'productos': productos,
        'puntos_totales': cliente.puntos_totales,
    }
    return render(request, 'clients/mi_panel_puntos.html', context)

@login_required
@require_POST
def canjear_producto(request, producto_id):
    """Canjear producto por puntos"""
    try:
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        producto = get_object_or_404(ProductoCanjeble, pk=producto_id)
        
        # Validar stock
        if producto.stock_disponible <= 0:
            return JsonResponse({
                'success': False,
                'error': 'Producto sin stock disponible'
            }, status=400)
        
        # Validar puntos
        if cliente.puntos_totales < producto.puntos_requeridos:
            return JsonResponse({
                'success': False,
                'error': f'Puntos insuficientes. Requiere {producto.puntos_requeridos} pts, tienes {cliente.puntos_totales} pts'
            }, status=400)
        
        # Crear canje
        canje = CanjeProducto.objects.create(
            cliente_id=cliente.id,
            producto_id=producto.id,
            puntos_gastados=producto.puntos_requeridos,
            estado=CanjeProducto.ESTADO_PENDIENTE
        )
        
        # Restar puntos al cliente
        cliente.puntos_totales -= producto.puntos_requeridos
        cliente.save()
        
        # Reducir stock del producto
        producto.stock_disponible -= 1
        producto.save()
        
        # Registrar transacción de puntos
        PuntosFidelizacion.objects.create(
            cliente_id=cliente.id,
            tipo=PuntosFidelizacion.TIPO_CANJE,
            puntos=-producto.puntos_requeridos,
            descripcion=f'Canje de {producto.nombre} (Canje #{canje.id})',
            canje_id=canje.id
        )
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Canje realizado exitosamente. Canje #{canje.id}',
            'canje_id': canje.id,
            'puntos_restantes': float(cliente.puntos_totales)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def canjes_cliente(request, cliente_id):
    """Historial de canjes del cliente"""
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    canjes = CanjeProducto.objects.filter(cliente_id=cliente_id).order_by('-fecha_canje')
    
    context = {
        'cliente': cliente,
        'canjes': canjes,
    }
    return render(request, 'clients/canjes_cliente.html', context)

@login_required
@check_user_role(allowed_roles=['Administrador'])
def administrar_productos_canjebles(request):
    """Administración de productos canjeables (solo admin)"""
    productos = ProductoCanjeble.objects.all().order_by('-fecha_creacion')
    
    context = {
        'productos': productos,
    }
    return render(request, 'clients/admin_productos_canjebles.html', context)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def crear_producto_canjeble(request):
    """Crear producto canjeble vía AJAX"""
    try:
        data = json.loads(request.body)
        
        producto = ProductoCanjeble.objects.create(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion', ''),
            puntos_requeridos=Decimal(data.get('puntos_requeridos', 0)),
            stock_disponible=int(data.get('stock_disponible', 0)),
            activo=data.get('activo', True)
        )
        
        return JsonResponse({
            'success': True,
            'id': producto.id,
            'nombre': producto.nombre,
            'puntos_requeridos': float(producto.puntos_requeridos),
            'stock_disponible': producto.stock_disponible,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def editar_producto_canjeble(request, producto_id):
    """Editar producto canjeble vía AJAX"""
    try:
        data = json.loads(request.body)
        producto = get_object_or_404(ProductoCanjeble, pk=producto_id)
        
        producto.nombre = data.get('nombre', producto.nombre)
        producto.descripcion = data.get('descripcion', producto.descripcion)
        producto.puntos_requeridos = Decimal(data.get('puntos_requeridos', producto.puntos_requeridos))
        producto.stock_disponible = int(data.get('stock_disponible', producto.stock_disponible))
        producto.activo = data.get('activo', producto.activo)
        producto.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Producto actualizado correctamente'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def eliminar_producto_canjeble(request, producto_id):
    """Eliminar producto canjeble vía AJAX"""
    try:
        producto = get_object_or_404(ProductoCanjeble, pk=producto_id)
        producto_nombre = producto.nombre
        producto.delete()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Producto "{producto_nombre}" eliminado correctamente'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def marcar_canje_entregado(request, canje_id):
    """Marcar canje como entregado"""
    try:
        from django.utils import timezone
        
        canje = get_object_or_404(CanjeProducto, pk=canje_id)
        canje.estado = CanjeProducto.ESTADO_COMPLETADO
        canje.fecha_entrega = timezone.now()
        canje.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Canje #{canje_id} marcado como entregado'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
