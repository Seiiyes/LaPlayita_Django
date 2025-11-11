from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib import messages
from decimal import Decimal
from datetime import datetime
import json

from users.decorators import check_user_role
from inventory.models import Producto, Lote
from clients.models import Cliente
from .models import Venta, VentaDetalle, Pedido, PedidoDetalle, Pago
from .forms import VentaForm, CarritoItemForm, ProductoSearchForm, PedidoForm
from django.utils import timezone


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pos_view(request):
    """
    Vista principal del Punto de Venta (POS).
    """
    productos = Producto.objects.filter(stock_actual__gt=0).select_related('categoria')
    clientes = Cliente.objects.all()
    venta_form = VentaForm()

    context = {
        'productos': productos,
        'clientes': clientes,
        'venta_form': venta_form,
    }
    return render(request, 'pos/pos_main.html', context)


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
@require_http_methods(["GET"])
def buscar_productos(request):
    """
    API para buscar productos por nombre o categoría.
    Retorna JSON con productos encontrados.
    """
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', None)

    productos = Producto.objects.filter(stock_actual__gt=0)

    if query:
        productos = productos.filter(
            nombre__icontains=query
        ) | Producto.objects.filter(
            descripcion__icontains=query
        )

    if categoria_id:
        try:
            productos = productos.filter(categoria_id=int(categoria_id))
        except (ValueError, TypeError):
            pass

    productos = productos.select_related('categoria')[:20]

    datos = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'precio': str(p.precio_unitario),
            'stock': p.stock_actual,
            'categoria': p.categoria.nombre,
            'descripcion': p.descripcion or '',
        }
        for p in productos
    ]

    return JsonResponse({'productos': datos})


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
@require_http_methods(["GET"])
def obtener_producto(request, producto_id):
    """
    API para obtener detalles de un producto específico.
    """
    try:
        producto = get_object_or_404(Producto, id=producto_id, stock_actual__gt=0)
        lotes = Lote.objects.filter(
            producto=producto,
            cantidad_disponible__gt=0
        ).order_by('fecha_caducidad')

        datos_lotes = []
        for lote in lotes:
            datos_lotes.append({
                'id': lote.id,
                'numero_lote': lote.numero_lote,
                'cantidad': lote.cantidad_disponible,
                'fecha_caducidad': lote.fecha_caducidad.isoformat() if lote.fecha_caducidad else None,
                'costo': str(lote.costo_unitario_lote),
            })

        datos = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': str(producto.precio_unitario),
            'stock': producto.stock_actual,
            'categoria': producto.categoria.nombre,
            'descripcion': producto.descripcion or '',
            'lotes': datos_lotes,
        }

        return JsonResponse(datos)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
@require_http_methods(["POST"])
def procesar_venta(request):
    """
    Procesa una venta completada desde el carrito.
    Espera JSON con los datos de la venta y los items del carrito.
    """
    try:
        datos = json.loads(request.body)

        # Validar datos
        if not datos.get('items') or len(datos['items']) == 0:
            return JsonResponse(
                {'error': 'El carrito está vacío'},
                status=400
            )

        cliente_id = datos.get('cliente_id')
        metodo_pago = datos.get('metodo_pago')
        canal_venta = datos.get('canal_venta')

        if not metodo_pago or not canal_venta:
            return JsonResponse(
                {'error': 'Debe seleccionar método de pago y canal de venta'},
                status=400
            )

        # Iniciar transacción
        with transaction.atomic():
            # Crear venta
            cliente = None
            if cliente_id:
                cliente = get_object_or_404(Cliente, id=cliente_id)

            venta = Venta.objects.create(
                usuario=request.user,
                cliente=cliente,
                canal_venta=canal_venta,
                total_venta=Decimal('0.00')
            )

            total_venta = Decimal('0.00')

            # Crear detalles de venta y actualizar stock
            for item in datos['items']:
                producto_id = item.get('producto_id')
                lote_id = item.get('lote_id')
                cantidad = int(item.get('cantidad', 1))

                producto = get_object_or_404(Producto, id=producto_id)
                lote = get_object_or_404(Lote, id=lote_id)

                # Validar stock
                if lote.cantidad_disponible < cantidad:
                    transaction.set_rollback(True)
                    return JsonResponse(
                        {'error': f'Stock insuficiente de {producto.nombre}'},
                        status=400
                    )

                subtotal = producto.precio_unitario * cantidad

                # Crear detalle de venta
                VentaDetalle.objects.create(
                    venta=venta,
                    producto=producto,
                    lote=lote,
                    cantidad=cantidad,
                    subtotal=subtotal
                )

                # Actualizar stock del lote
                lote.cantidad_disponible -= cantidad
                lote.save(update_fields=['cantidad_disponible'])

                # Actualizar stock y costo promedio del producto
                producto.actualizar_costo_promedio_y_stock()

                total_venta += subtotal

            # Actualizar total de venta
            venta.total_venta = total_venta
            venta.save(update_fields=['total_venta'])

            # Registrar pago asociado a la venta (tabla 'pago' en la BD)
            Pago.objects.create(
                venta=venta,
                monto=total_venta,
                metodo_pago=metodo_pago,
                fecha_pago=timezone.now(),
                estado='completado'
            )

        messages.success(request, f'Venta #{venta.id} procesada exitosamente')
        return JsonResponse({
            'success': True,
            'venta_id': venta.id,
            'total': str(total_venta),
            'mensaje': f'Venta #{venta.id} completada'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def venta_detalle(request, venta_id):
    """
    Muestra los detalles de una venta específica.
    """
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = VentaDetalle.objects.filter(venta=venta).select_related('producto', 'lote')
    pago = Pago.objects.filter(venta=venta).first()

    context = {
        'venta': venta,
        'detalles': detalles,
        'pago': pago,
    }
    return render(request, 'pos/venta_detalle.html', context)


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def listar_ventas(request):
    """
    Lista todas las ventas con paginación y filtros.
    """
    ventas = Venta.objects.all().select_related('cliente', 'usuario').order_by('-fecha_venta')

    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    metodo_pago = request.GET.get('metodo_pago')
    usuario_id = request.GET.get('usuario_id')

    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
            ventas = ventas.filter(fecha_venta__gte=fecha_inicio_dt)
        except (ValueError, TypeError):
            pass

    if fecha_fin:
        try:
            fecha_fin_dt = datetime.fromisoformat(fecha_fin)
            ventas = ventas.filter(fecha_venta__lte=fecha_fin_dt)
        except (ValueError, TypeError):
            pass

    if metodo_pago:
        # Filtrar ventas por método de pago presente en la tabla `pago`
        ventas = ventas.filter(pago__metodo_pago=metodo_pago)

    if usuario_id:
        try:
            ventas = ventas.filter(usuario_id=int(usuario_id))
        except (ValueError, TypeError):
            pass

    context = {
        'ventas': ventas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'metodo_pago': metodo_pago,
    }
    return render(request, 'pos/listar_ventas.html', context)