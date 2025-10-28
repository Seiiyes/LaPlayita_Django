# C:\laplayita\la_playita_project\core\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.contrib import messages
from datetime import date, timedelta
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.utils import timezone

from .models import Producto, Lote, Categoria, MovimientoInventario, Cliente, Venta, VentaDetalle
from .forms import VendedorRegistrationForm, ProductoForm, LoteForm, CategoriaForm
from .models import Reabastecimiento, ReabastecimientoDetalle, Proveedor
from .forms import ReabastecimientoForm, ReabastecimientoDetalleFormSet
from django.db import transaction, connection
from django.contrib.auth.views import LoginView
from .decorators import check_user_role


def send_supply_request_email(reabastecimiento):
    proveedor = reabastecimiento.proveedor
    if proveedor.correo:
        subject = f'Solicitud de Reabastecimiento #{reabastecimiento.id}'
        
        message = f"""
        Hola {proveedor.nombre_empresa},

        Se ha generado una nueva solicitud de reabastecimiento.

        Detalles:
        ID de Reabastecimiento: {reabastecimiento.id}
        Fecha de Solicitud: {reabastecimiento.fecha.strftime('%d/%m/%Y %H:%M')}
        Observaciones: {reabastecimiento.observaciones or 'N/A'}

        Productos solicitados:
        """
        
        for detalle in reabastecimiento.reabastecimientodetalle_set.all():
            message += f"- {detalle.producto.nombre}: {detalle.cantidad} unidades\n"
            
        message += "\nGracias,\nEl equipo de La Playita."

        # TODO: Configure EMAIL_HOST_USER in settings.py
        send_mail(
            subject,
            message,
            'no-reply@laplayita.com', 
            [proveedor.correo],
            fail_silently=False,
        )

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


# ----------------------------------------------
# Vistas de Autenticación y Flujo
# ----------------------------------------------

def landing_view(request):
    """Vista de la página de inicio."""
    return render(request, 'core/landing.html')

@never_cache
@login_required
def login_redirect_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.rol and user.rol.nombre in ['Administrador', 'Vendedor']:
            return redirect('dashboard')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = VendedorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = VendedorRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# ----------------------------------------------
# Dashboard
# ----------------------------------------------

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def dashboard_view(request):
    productos_count = Producto.objects.count()
    productos_bajos_stock = Producto.objects.filter(stock_actual__lt=models.F('stock_minimo')).count()
    # Contador de reabastecimientos para administradores
    reabastecimientos_count = 0
    if request.user and request.user.rol and request.user.rol.nombre == 'Administrador':
        try:
            reabastecimientos_count = Reabastecimiento.objects.count()
        except Exception:
            reabastecimientos_count = 0
    context = {
        'total_productos': productos_count,
        'productos_bajos_stock': productos_bajos_stock,
        'reabastecimientos_count': reabastecimientos_count,
    }
    return render(request, 'core/dashboard.html', context)


# ----------------------------------------------
# Vistas de Punto de Venta (POS)
# ----------------------------------------------

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pos_view(request):
    """
    Vista para la interfaz de Punto de Venta (POS).
    """
    productos = Producto.objects.filter(stock_actual__gt=0).order_by('nombre')
    clientes = Cliente.objects.all().order_by('nombres', 'apellidos')
    
    context = {
        'productos': productos,
        'clientes': clientes,
    }
    return render(request, 'core/pos.html', context)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def procesar_venta(request):
    try:
        data = json.loads(request.body)
        
        with transaction.atomic(): # Start transaction
            # Get all product IDs from the cart
            product_ids = [item['id'] for item in data['items']]
            
            # Lock the products for this sale to prevent deadlocks
            # We map them by ID for easy access
            productos_a_vender = {
                p.id: p for p in Producto.objects.select_for_update().filter(id__in=product_ids)
            }

            cliente_id = data.get('cliente_id')
            cliente = Cliente.objects.get(pk=cliente_id) if cliente_id else None

            venta = Venta.objects.create(
                fecha_venta=timezone.now(),
                metodo_pago=data['metodo_pago'],
                canal_venta='local',
                cliente=cliente,
                usuario=request.user,
                total_venta=0
            )

            total_venta_calculado = 0
            for item in data['items']:
                producto_id = int(item['id'])
                producto = productos_a_vender.get(producto_id)
                
                if not producto:
                    raise Exception(f"Producto con ID {producto_id} no encontrado.")

                cantidad_a_vender = int(item['cantidad'])

                # We must re-check stock inside the transaction to be safe
                if producto.stock_actual < cantidad_a_vender:
                    raise Exception(f"Stock insuficiente para {producto.nombre} (Stock: {producto.stock_actual}, Solicitado: {cantidad_a_vender})")

                lotes = Lote.objects.filter(
                    producto=producto, 
                    cantidad_disponible__gt=0
                ).order_by('fecha_caducidad')

                cantidad_restante_por_vender = cantidad_a_vender
                for lote in lotes:
                    if cantidad_restante_por_vender == 0:
                        break

                    cantidad_a_tomar_del_lote = min(lote.cantidad_disponible, cantidad_restante_por_vender)
                    
                    VentaDetalle.objects.create(
                        venta=venta,
                        producto=producto,
                        lote=lote,
                        cantidad=cantidad_a_tomar_del_lote,
                        subtotal=cantidad_a_tomar_del_lote * producto.precio_unitario
                    )

                    lote.cantidad_disponible -= cantidad_a_tomar_del_lote
                    lote.save()

                    total_venta_calculado += cantidad_a_tomar_del_lote * producto.precio_unitario
                    cantidad_restante_por_vender -= cantidad_a_tomar_del_lote
            
            if cantidad_restante_por_vender > 0:
                # This should not happen if the initial stock check is correct, but it's a good safeguard.
                raise Exception(f"No se pudo satisfacer la cantidad completa para {producto.nombre}. Error de lógica de stock.")

            venta.total_venta = total_venta_calculado
            venta.save()

        return JsonResponse({'message': 'Venta completada exitosamente', 'venta_id': venta.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ----------------------------------------------
# Vistas de Gestión de Productos
# ----------------------------------------------

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def inventario_list(request):
    today = date.today()

    # Subconsulta para obtener el código del lote MÁS RECIENTE con stock
    recent_lot_subquery = Lote.objects.filter(
        producto=models.OuterRef('pk'),
        cantidad_disponible__gt=0
    ).order_by('-fecha_entrada').values('numero_lote')[:1]

    # Subconsulta para obtener el proveedor del lote MÁS RECIENTE
    recent_lot_supplier_subquery = Lote.objects.filter(
        producto=models.OuterRef('pk'),
        cantidad_disponible__gt=0
    ).order_by('-fecha_entrada').values('reabastecimiento_detalle__reabastecimiento__proveedor__nombre_empresa')[:1]

    # Anotamos los productos con la información de los lotes
    productos = Producto.objects.annotate(
        vencimiento_proximo=models.Min('lote__fecha_caducidad', filter=models.Q(lote__cantidad_disponible__gt=0)),
        lote_mas_reciente=models.Subquery(recent_lot_subquery),
        proveedor_lote_mas_reciente=models.Subquery(recent_lot_supplier_subquery)
    ).select_related('categoria').all()

    form = ProductoForm()
    categoria_form = CategoriaForm()
    
    context = {
        'productos': productos,
        'form': form,
        'categoria_form': categoria_form,
        'today': today,
        'alert_days_yellow': 60,
        'alert_days_red': 30,
    }
    return render(request, 'core/inventario_list.html', context)

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def alertas_stock_list(request):
    productos = Producto.objects.filter(stock_actual__lt=models.F('stock_minimo')).select_related('categoria')
    form = ProductoForm()
    context = {
        'productos': productos,
        'form': form,
        'alertas_stock': True,
    }
    return render(request, 'core/inventario_list.html', context)

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def producto_create(request):
    form = ProductoForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto creado exitosamente.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label}: {error}")
    return redirect('inventario_list')

@login_required
def producto_detail_json(request, pk):
    """
    Devuelve los detalles de un producto en formato JSON para la edición en modal.
    """
    producto = get_object_or_404(Producto, pk=pk)
    data = {
        'id': producto.pk,
        'nombre': producto.nombre,
        'precio_unitario': str(producto.precio_unitario),
        'descripcion': producto.descripcion,
        'stock_minimo': producto.stock_minimo,
        'categoria_id': producto.categoria_id,
    }
    return JsonResponse(data)

@never_cache
@login_required
@require_POST # This view now only handles POST requests
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST, instance=producto)
    if form.is_valid():
        producto = form.save()
        return JsonResponse({
            'id': producto.pk,
            'nombre': producto.nombre,
            'categoria_nombre': producto.categoria.nombre,
            'precio_unitario': str(producto.precio_unitario),
            'stock_actual': producto.stock_actual,
            'stock_minimo': producto.stock_minimo,
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return redirect('inventario_list')

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def categoria_create(request):
    form = CategoriaForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada exitosamente.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label}: {error}")
    return redirect('inventario_list')

# ----------------------------------------------
# Vistas de Gestión de Lotes (Trazabilidad)
# ----------------------------------------------

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def lote_list(request, producto_pk):
    producto = get_object_or_404(Producto, pk=producto_pk)
    lotes = Lote.objects.filter(producto=producto).order_by('-fecha_entrada')
    form = LoteForm(initial={'producto': producto})
    
    today = date.today()
    thirty_days_from_now = today + timedelta(days=30)

    context = {
        'lotes': lotes,
        'producto': producto,
        'form': form,
        'today': today,
        'thirty_days_from_now': thirty_days_from_now,
    }
    return render(request, 'core/lote_list.html', context)


@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_list(request):
    """
    Lista simple de reabastecimientos.
    """
    reabs = (
        Reabastecimiento.objects
        .exclude(estado=Reabastecimiento.ESTADO_CANCELADO)
        .select_related('proveedor')
        .prefetch_related(
            'reabastecimientodetalle_set__producto',
            'reabastecimientodetalle_set__producto__categoria',
            'reabastecimientodetalle_set__lote_set',
            'reabastecimientodetalle_set__lote_set__ventadetalle_set'
        )
        .order_by('-fecha'))
    
    for reab in reabs:
        reab.tiene_ventas = any(
            lote.ventadetalle_set.exists()
            for detalle in reab.reabastecimientodetalle_set.all()
            for lote in detalle.lote_set.all()
        )

    form = None
    formset = None
    if request.user.is_authenticated and getattr(request.user, 'rol', None) and request.user.rol.nombre == 'Administrador':
        form = ReabastecimientoForm()
        formset = ReabastecimientoDetalleFormSet(queryset=ReabastecimientoDetalle.objects.none())

    productos_data = []
    try:
        productos_qs = Producto.objects.all().only('id', 'precio_unitario')
        for p in productos_qs:
            productos_data.append({'id': p.id, 'precio_unitario': float(p.precio_unitario) if p.precio_unitario is not None else 0.0})
    except Exception:
        productos_data = []

    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    all_products_data = list(Producto.objects.values('id', 'nombre'))

    context = {
        'reabastecimientos': reabs,
        'form': form,
        'formset': formset,
        'products_data': productos_data,
        'products_json': json.dumps(productos_data),
        'all_products_json': json.dumps(all_products_data),
        'categorias': categorias,
        'productos': productos,
    }
    return render(request, 'core/reabastecimiento_list.html', context)


@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_create(request):
    """
    Crear un reabastecimiento con múltiples detalles.
    No crea lotes ni actualiza stock, solo crea la solicitud.
    Envía un correo al proveedor si el estado es 'solicitado'.
    Responde con JSON para solicitudes AJAX.
    """
    if request.method == 'POST':
        form = ReabastecimientoForm(request.POST)
        formset = ReabastecimientoDetalleFormSet(request.POST, queryset=ReabastecimientoDetalle.objects.none())
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    reab = form.save(commit=False)
                    
                    total = 0
                    details_for_creation = []
                    for detalle_form in formset.cleaned_data:
                        if detalle_form and not detalle_form.get('DELETE', False):
                            cantidad = detalle_form['cantidad']
                            costo_unitario = detalle_form['costo_unitario']
                            total += cantidad * float(costo_unitario)
                            details_for_creation.append(detalle_form)

                    if not details_for_creation:
                        return JsonResponse({'error': 'Debe agregar al menos un detalle de producto.'}, status=400)

                    reab.costo_total = total
                    reab.save()

                    detalles_data = []
                    for detalle_form in details_for_creation:
                        producto = detalle_form['producto']
                        detalle = ReabastecimientoDetalle.objects.create(
                            reabastecimiento=reab,
                            producto=producto,
                            cantidad=detalle_form['cantidad'],
                            costo_unitario=detalle_form['costo_unitario'],
                            fecha_caducidad=detalle_form['fecha_caducidad']
                        )
                        detalles_data.append({
                            'producto_nombre': producto.nombre,
                            'categoria_nombre': producto.categoria.nombre,
                            'cantidad': detalle.cantidad,
                            'costo_unitario': float(detalle.costo_unitario),
                            'subtotal': float(detalle.cantidad * detalle.costo_unitario),
                            'estado_lote': 'No recibido'
                        })

                    if reab.estado == Reabastecimiento.ESTADO_SOLICITADO:
                        try:
                            send_supply_request_email(reab)
                        except Exception as email_error:
                            print(f"Error sending email: {email_error}")

                    return JsonResponse({
                        'id': reab.id,
                        'fecha': reab.fecha.strftime('%d/%m/%Y %H:%M'),
                        'proveedor': reab.proveedor.nombre_empresa,
                        'costo_total': float(reab.costo_total),
                        'forma_pago': reab.get_forma_pago_display(),
                        'estado': reab.get_estado_display(),
                        'observaciones': reab.observaciones,
                        'detalles': detalles_data
                    })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else: 
            errors = json.loads(form.errors.as_json())
            formset_errors = [f.errors for f in formset.forms if f.errors]
            return JsonResponse({'errors': errors, 'formset_errors': formset_errors}, status=400)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_recibir(request, pk):
    """
    Marcar un reabastecimiento como 'recibido' y crear los lotes correspondientes,
    actualizando así el stock de los productos.
    """
    try:
        with transaction.atomic():
            reab = get_object_or_404(Reabastecimiento, pk=pk)
            
            if reab.estado == Reabastecimiento.ESTADO_RECIBIDO:
                return JsonResponse({'error': 'Este reabastecimiento ya ha sido recibido.'}, status=400)

            reab.estado = Reabastecimiento.ESTADO_RECIBIDO
            reab.save()

            for detalle in reab.reabastecimientodetalle_set.all():
                if not detalle.fecha_caducidad:
                    return JsonResponse({'error': f'El producto {detalle.producto.nombre} no tiene fecha de caducidad.'}, status=400)

                numero_lote = f"R{reab.pk}-P{detalle.producto.pk}-{detalle.pk}"
                Lote.objects.create(
                    producto=detalle.producto,
                    reabastecimiento_detalle=detalle,
                    numero_lote=numero_lote,
                    cantidad_disponible=detalle.cantidad,
                    costo_unitario_lote=detalle.costo_unitario,
                    fecha_caducidad=detalle.fecha_caducidad
                )
            
            return JsonResponse({'message': 'Reabastecimiento marcado como recibido y stock actualizado.', 'estado': reab.get_estado_display()})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def lote_create(request, producto_pk):
    producto = get_object_or_404(Producto, pk=producto_pk)
    form = LoteForm(request.POST)
    if form.is_valid():
        lote = form.save(commit=False)
        lote.producto = producto
        lote.save()
        messages.success(request, 'Lote registrado exitosamente.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label}: {error}")
    return redirect('lote_list', producto_pk=producto.pk)

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def lote_update(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method == 'POST':
        form = LoteForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lote actualizado exitosamente.')
            return redirect('lote_list', producto_pk=lote.producto.pk)
    else:
        form = LoteForm(instance=lote)
    return render(request, 'core/lote_form.html', {'form': form, 'lote': lote})

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def lote_delete(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    producto_pk = lote.producto.pk
    lote.delete()
    messages.success(request, 'Lote eliminado exitosamente.')
    return redirect('lote_list', producto_pk=producto_pk)

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_editar(request, pk):
    """Vista para editar un reabastecimiento."""
    try:
        reab = Reabastecimiento.objects.prefetch_related(
            'reabastecimientodetalle_set__producto',
            'reabastecimientodetalle_set__lote_set'
        ).get(pk=pk)

        if reab.estado == Reabastecimiento.ESTADO_RECIBIDO:
            return JsonResponse({
                'error': 'No se puede editar un reabastecimiento que ya ha sido recibido.'
            }, status=400)
        
        if any(lote.ventadetalle_set.exists()
               for detalle in reab.reabastecimientodetalle_set.all()
               for lote in detalle.lote_set.all()):
            return JsonResponse({
                'error': 'No se puede editar este reabastecimiento porque tiene productos vendidos'
            }, status=400)
        
        data = {
            'id': reab.id,
            'proveedor_id': reab.proveedor_id,
            'fecha': reab.fecha.isoformat(),
            'forma_pago': reab.forma_pago,
            'observaciones': reab.observaciones,
            'detalles': [{
                'id': detalle.id,
                'producto_id': detalle.producto_id,
                'producto_nombre': detalle.producto.nombre,  # <-- Añadido para el frontend
                'cantidad': detalle.cantidad,
                'costo_unitario': str(detalle.costo_unitario),
                'fecha_caducidad': detalle.fecha_caducidad.isoformat() if detalle.fecha_caducidad else None
            } for detalle in reab.reabastecimientodetalle_set.all()]
        }
        return JsonResponse(data)
    except Reabastecimiento.DoesNotExist:
        return JsonResponse({'error': 'Reabastecimiento no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_update(request, pk):
    """
    Actualizar un reabastecimiento con múltiples detalles.
    Responde con JSON para solicitudes AJAX.
    """
    try:
        with transaction.atomic():
            reab = get_object_or_404(Reabastecimiento, pk=pk)

            if reab.estado == Reabastecimiento.ESTADO_RECIBIDO:
                return JsonResponse({
                    'error': 'No se puede editar un reabastecimiento que ya ha sido recibido.'
                }, status=400)
            
            if any(lote.ventadetalle_set.exists() for detalle in reab.reabastecimientodetalle_set.all() for lote in detalle.lote_set.all()):
                return JsonResponse({'error': 'No se puede editar un reabastecimiento con productos vendidos.'}, status=400)

            form = ReabastecimientoForm(request.POST, instance=reab)
            formset = ReabastecimientoDetalleFormSet(request.POST, instance=reab)

            if form.is_valid() and formset.is_valid():
                reab_instance = form.save()

                # Handle deletions
                for form_detalle in formset.deleted_forms:
                    if form_detalle.instance.pk:
                        form_detalle.instance.delete()

                # Handle new and updated
                detalles_actualizados = []
                total = 0
                for form_detalle in formset.forms:
                    if form_detalle.cleaned_data and not form_detalle.cleaned_data.get('DELETE', False):
                        detalle = form_detalle.save(commit=False)
                        detalle.reabastecimiento = reab_instance
                        detalle.save()
                        
                        cantidad = form_detalle.cleaned_data['cantidad']
                        costo_unitario = form_detalle.cleaned_data['costo_unitario']
                        total += cantidad * float(costo_unitario)
                        detalles_actualizados.append(detalle)

                if not detalles_actualizados:
                    return JsonResponse({'error': 'Debe agregar al menos un detalle de producto.'}, status=400)

                reab_instance.costo_total = total
                reab_instance.save()

                if reab_instance.estado == Reabastecimiento.ESTADO_SOLICITADO:
                    try:
                        send_supply_request_email(reab_instance)
                    except Exception as email_error:
                        print(f"Error sending email on update: {email_error}")

                return JsonResponse({
                    'id': reab_instance.id,
                    'fecha': reab_instance.fecha.strftime('%d/%m/%Y %H:%M'),
                    'proveedor': reab_instance.proveedor.nombre_empresa,
                    'costo_total': float(reab_instance.costo_total),
                    'forma_pago': reab_instance.get_forma_pago_display(),
                    'estado': reab_instance.get_estado_display(),
                    'observaciones': reab_instance.observaciones,
                })
            else:
                errors = json.loads(form.errors.as_json())
                formset_errors = [f.errors for f in formset.forms if f.errors]
                return JsonResponse({'errors': errors, 'formset_errors': formset_errors}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_eliminar(request, pk):
    """Vista para eliminar un reabastecimiento (borrado físico)."""
    try:
        with transaction.atomic():
            reab = get_object_or_404(Reabastecimiento, pk=pk)
            
            # Check if any associated lots have been sold
            if Lote.objects.filter(reabastecimiento_detalle__reabastecimiento=reab, ventadetalle__isnull=False).exists():
                return JsonResponse({
                    'error': 'No se puede eliminar este reabastecimiento porque tiene productos vendidos'
                }, status=400)
            
            # Delete associated Lotes first, which will also update stock
            Lote.objects.filter(reabastecimiento_detalle__reabastecimiento=reab).delete()

            with connection.cursor() as cursor:
                # Delete from movimiento_inventario to prevent ON DELETE SET NULL issue
                cursor.execute("DELETE FROM movimiento_inventario WHERE reabastecimiento_id = %s", [pk])
                
                # Now, delete the reabastecimiento. The DB will cascade to reabastecimiento_detalle.
                cursor.execute("DELETE FROM reabastecimiento WHERE id = %s", [pk])
            
            return JsonResponse({'message': 'Reabastecimiento eliminado correctamente'})
            
    except Reabastecimiento.DoesNotExist:
        return JsonResponse({'error': 'Reabastecimiento no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reportes_home(request):
    """
    Vista de marcador de posición para la página de reportes.
    """
    return render(request, 'core/placeholder.html')

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def cliente_list(request):
    """
    Vista de marcador de posición para la lista de clientes.
    """
    return render(request, 'core/placeholder.html')

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def proveedor_create_ajax(request):
    """
    Vista para crear un proveedor vía AJAX.
    """
    try:
        data = json.loads(request.body)
        proveedor = Proveedor.objects.create(
            nombre_empresa=data['nombre_empresa'],
            telefono=data.get('telefono', ''),
            correo=data.get('correo', ''),
            direccion=data.get('direccion', '')
        )
        return JsonResponse({
            'id': proveedor.id,
            'nombre_empresa': proveedor.nombre_empresa
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def categoria_create_ajax(request):
    """
    Vista para crear una categoría vía AJAX.
    """
    try:
        data = json.loads(request.body)
        categoria = Categoria.objects.create(
            nombre=data['nombre']
        )
        return JsonResponse({
            'id': categoria.id,
            'nombre': categoria.nombre
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def producto_create_ajax(request):
    """
    Vista para crear un producto vía AJAX.
    """
    try:
        data = json.loads(request.body)
        producto = Producto.objects.create(
            nombre=data['nombre'],
            categoria_id=data['categoria'],
            precio_unitario=data['precio_unitario'],
            stock_minimo=data['stock_minimo'],
            stock_actual=0,
            descripcion=data.get('descripcion', '')
        )
        return JsonResponse({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio_unitario': float(producto.precio_unitario)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
