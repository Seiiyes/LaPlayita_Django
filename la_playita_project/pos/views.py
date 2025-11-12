from django.shortcuts import render
import json
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from inventory.models import Producto, Lote
from clients.models import Cliente
from .models import Venta, VentaDetalle, Pago
from .forms import ProductoSearchForm, VentaForm
from users.decorators import check_user_role


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pos_view(request):
    """Vista principal del Punto de Venta (POS)"""
    productos = Producto.objects.filter(stock_actual__gt=0).select_related('categoria').order_by('nombre')
    search_form = ProductoSearchForm()
    venta_form = VentaForm()
    
    context = {
        'productos': productos,
        'search_form': search_form,
        'venta_form': venta_form,
    }
    return render(request, 'pos/pos_main.html', context)

@login_required
def buscar_productos(request):
    """API para buscar productos por nombre o categoría"""
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query, stock_actual__gt=0).select_related('categoria')
    
    productos_data = [{
        'id': p.id,
        'nombre': p.nombre,
        'precio': p.precio_unitario,
        'stock': p.stock_actual,
        'categoria': p.categoria.nombre if p.categoria else 'Sin categoría',
        'descripcion': p.descripcion or ''
    } for p in productos]
    
    return JsonResponse({'productos': productos_data})


@login_required
def obtener_producto(request, producto_id):
    """API para obtener detalles de un producto, incluyendo sus lotes"""
    producto = get_object_or_404(Producto, pk=producto_id)
    lotes = Lote.objects.filter(producto=producto, cantidad_disponible__gt=0).order_by('fecha_caducidad')
    
    producto_data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio_unitario,
        'stock': producto.stock_actual,
        'categoria': producto.categoria.nombre if producto.categoria else 'Sin categoría',
        'descripcion': producto.descripcion or '',
        'lotes': [{
            'id': lote.id,
            'numero_lote': lote.numero_lote,
            'cantidad': lote.cantidad_disponible,
            'fecha_caducidad': lote.fecha_caducidad.strftime('%Y-%m-%d') if lote.fecha_caducidad else 'N/A'
        } for lote in lotes]
    }
    
    return JsonResponse(producto_data)


@login_required
@require_POST
@transaction.atomic
def procesar_venta(request):
    """API para procesar una venta desde el carrito"""
    try:
        data = json.loads(request.body)
        cart_items = data.get('items', [])

        if not cart_items:
            return JsonResponse({'success': False, 'error': 'El carrito está vacío.'}, status=400)

        # CORRECCIÓN: Si no se proporciona un cliente_id, se asigna el cliente
        # por defecto "Consumidor Final" (asumiendo que tiene el ID 1).
        # Esto evita el error "Column 'cliente_id' cannot be null".
        cliente_id = data.get('cliente_id')
        if cliente_id:
            cliente = get_object_or_404(Cliente, pk=cliente_id)
        else:
            cliente = get_object_or_404(Cliente, pk=1) # Asigna el cliente por defecto

        # Calcular total
        total_venta = sum(Decimal(item['precio']) * int(item['cantidad']) for item in cart_items)
        subtotal = total_venta / Decimal('1.19')

        # Crear la venta
        nueva_venta = Venta.objects.create(
            cliente=cliente,
            usuario=request.user,
            canal_venta=data['canal_venta'],
            total_venta=total_venta
        )

        # Crear el pago asociado
        Pago.objects.create(
            venta=nueva_venta,
            monto=total_venta,
            metodo_pago=data['metodo_pago'],
            estado='completado'
        )

        # Crear detalles y actualizar stock
        for item in cart_items:
            producto = get_object_or_404(Producto, pk=item['producto_id'])
            lote = get_object_or_404(Lote, pk=item['lote_id'])
            cantidad = int(item['cantidad'])

            if lote.cantidad_disponible < cantidad:
                raise Exception(f"Stock insuficiente para el lote {lote.numero_lote} de {producto.nombre}")

            VentaDetalle.objects.create(
                venta=nueva_venta,
                producto=producto,
                lote=lote,
                cantidad=cantidad,
                subtotal=Decimal(item['precio']) * cantidad
            )

            # Actualizar stock del lote y del producto
            lote.cantidad_disponible -= cantidad
            lote.save()
            producto.stock_actual -= cantidad
            producto.save()

        return JsonResponse({'success': True, 'venta_id': nueva_venta.id, 'mensaje': f'Venta #{nueva_venta.id} procesada con éxito.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def venta_detalle(request, venta_id):
    """Vista para mostrar el detalle de una venta completada"""
    venta = get_object_or_404(Venta.objects.select_related('cliente', 'usuario'), pk=venta_id)
    detalles = VentaDetalle.objects.filter(venta=venta).select_related('producto', 'lote')
    pago = Pago.objects.filter(venta=venta).first()
    
    # Calcular impuesto (19%)
    impuesto = float(venta.total_venta) * 0.19
    
    return render(request, 'pos/venta_detalle.html', {
        'venta': venta, 
        'detalles': detalles, 
        'pago': pago,
        'impuesto': impuesto
    })


@login_required
def obtener_clientes(request):
    """API para obtener lista de clientes para el POS"""
    try:
        clientes = list(Cliente.objects.all().values('id', 'nombres', 'apellidos').order_by('nombres'))
        
        clientes_formateados = []
        for c in clientes:
            nombre_completo = f"{c['nombres']} {c['apellidos']}".strip()
            clientes_formateados.append({
                'id': c['id'],
                'nombre': nombre_completo
            })
        
        return JsonResponse({
            'success': True,
            'clientes': clientes_formateados,
            'total': len(clientes_formateados)
        })
        
    except Exception as e:
        import traceback
        print(f"[ERROR OBTENER_CLIENTES] {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'clientes': []
        }, status=500)


@login_required
def listar_ventas(request):
    """Vista para listar todas las ventas con filtros"""
    ventas = Venta.objects.all().select_related('cliente', 'usuario').order_by('-fecha_venta')
    return render(request, 'pos/listar_ventas.html', {'ventas': ventas})