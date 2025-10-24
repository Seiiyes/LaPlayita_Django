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

from .models import Producto, Lote, Categoria
from .forms import VendedorRegistrationForm, ProductoForm, LoteForm, CategoriaForm
from .models import Reabastecimiento, ReabastecimientoDetalle, Proveedor
from .forms import ReabastecimientoForm, ReabastecimientoDetalleFormSet
from django.db import transaction
from django.contrib.auth.views import LoginView
from .decorators import check_user_role


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
        # Nombres de campo alineados con la plantilla: lote_mas_reciente / proveedor_lote_mas_reciente
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

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('inventario_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'core/producto_form.html', {'form': form, 'producto': producto})

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador']) # Solo Admin puede eliminar
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
@check_user_role(allowed_roles=['Administrador']) # Solo Admin
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
    # Obtener reabastecimientos con sus detalles, productos y verificar ventas asociadas
    reabs = (Reabastecimiento.objects
             .select_related('proveedor')
             .prefetch_related(
                 'reabastecimientodetalle_set__producto',
                 'reabastecimientodetalle_set__producto__categoria',
                 'reabastecimientodetalle_set__lote_set',
                 'reabastecimientodetalle_set__lote_set__ventadetalle_set'
             )
             .order_by('-fecha'))
    
    # Agregar atributo tiene_ventas a cada reabastecimiento
    for reab in reabs:
        reab.tiene_ventas = any(
            lote.ventadetalle_set.exists()
            for detalle in reab.reabastecimientodetalle_set.all()
            for lote in detalle.lote_set.all()
        )

    # Preparar el formulario y formset para el modal sólo si el usuario es administrador
    form = None
    formset = None
    if request.user.is_authenticated and getattr(request.user, 'rol', None) and request.user.rol.nombre == 'Administrador':
        form = ReabastecimientoForm()
        formset = ReabastecimientoDetalleFormSet(queryset=ReabastecimientoDetalle.objects.none())

    # Datos de productos para ayudar al auto-relleno de costo unitario en el modal
    productos_data = []
    try:
        from .models import Producto
        productos_qs = Producto.objects.all().only('id', 'precio_unitario')
        for p in productos_qs:
            productos_data.append({'id': p.id, 'precio_unitario': float(p.precio_unitario) if p.precio_unitario is not None else 0.0})
    except Exception:
        productos_data = []

    # Obtener categorías para el modal de nuevo producto
    categorias = Categoria.objects.all()

    context = {
        'reabastecimientos': reabs,
        'form': form,
        'formset': formset,
        'products_data': productos_data,
        'products_json': json.dumps(productos_data),
        'categorias': categorias,
    }
    return render(request, 'core/reabastecimiento_list.html', context)


@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reabastecimiento_create(request):
    """
    Crear un reabastecimiento con múltiples detalles. Por cada detalle se creará un lote asociado.
    Todo el proceso es atómico para no dejar la DB en estado inconsistente.
    """
    if request.method == 'POST':
        form = ReabastecimientoForm(request.POST)
        formset = ReabastecimientoDetalleFormSet(request.POST, queryset=ReabastecimientoDetalle.objects.none())
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    reab = form.save(commit=False)
                    # Si no se proporciona fecha, use ahora
                    if not reab.fecha:
                        from django.utils import timezone
                        reab.fecha = timezone.now()
                    # calcular costo_total provisional
                    reab.costo_total = 0
                    reab.save()

                    total = 0
                    detalles_to_create = []
                    for detalle_form in formset.cleaned_data:
                        if detalle_form and not detalle_form.get('DELETE', False):
                            producto = detalle_form['producto']
                            cantidad = detalle_form['cantidad']
                            costo_unitario = detalle_form['costo_unitario']
                            fecha_caducidad = detalle_form.get('fecha_caducidad')

                            detalle = ReabastecimientoDetalle.objects.create(
                                reabastecimiento=reab,
                                producto=producto,
                                cantidad=cantidad,
                                costo_unitario=costo_unitario
                            )

                            # Crear lote asociado
                            numero_lote = f"R{reab.pk}-P{producto.pk}-{detalle.pk}"
                            Lote.objects.create(
                                producto=producto,
                                reabastecimiento_detalle=detalle,
                                numero_lote=numero_lote,
                                cantidad_disponible=cantidad,
                                costo_unitario_lote=costo_unitario,
                                fecha_caducidad=fecha_caducidad
                            )

                            total += cantidad * float(costo_unitario)

                    # Actualizar costo total
                    reab.costo_total = total
                    reab.save()

                    messages.success(request, 'Reabastecimiento creado correctamente.')
                    return redirect('reabastecimiento_list')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al crear el reabastecimiento: {e}')
    else:
        form = ReabastecimientoForm()
        formset = ReabastecimientoDetalleFormSet(queryset=ReabastecimientoDetalle.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'core/reabastecimiento_form.html', context)

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador']) # Solo Admin
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
@check_user_role(allowed_roles=['Administrador']) # Solo Admin
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
@check_user_role(allowed_roles=['Administrador']) # Solo Admin
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
        
        # Verificar si hay productos vendidos
        if any(lote.ventadetalle_set.exists()
               for detalle in reab.reabastecimientodetalle_set.all()
               for lote in detalle.lote_set.all()):
            return JsonResponse({
                'error': 'No se puede editar este reabastecimiento porque tiene productos vendidos'
            }, status=400)
        
        # Por ahora solo retornamos los datos básicos
        data = {
            'id': reab.id,
            'proveedor_id': reab.proveedor_id,
            'fecha': reab.fecha.isoformat(),
            'forma_pago': reab.forma_pago,
            'observaciones': reab.observaciones,
            'detalles': [{
                'id': detalle.id,
                'producto_id': detalle.producto_id,
                'cantidad': detalle.cantidad,
                'costo_unitario': str(detalle.costo_unitario),
                'fecha_caducidad': detalle.lote_set.first().fecha_caducidad.isoformat() if detalle.lote_set.first() else None
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
def reabastecimiento_eliminar(request, pk):
    """Vista para eliminar un reabastecimiento."""
    try:
        with transaction.atomic():
            reab = get_object_or_404(Reabastecimiento, pk=pk)
            
            # Verificar si hay ventas asociadas a cualquier lote del reabastecimiento
            tiene_ventas = any(
                lote.ventadetalle_set.exists()
                for detalle in reab.reabastecimientodetalle_set.all()
                for lote in detalle.lote_set.all()
            )
            
            if tiene_ventas:
                return JsonResponse({
                    'error': 'No se puede eliminar este reabastecimiento porque tiene productos vendidos'
                }, status=400)
            
            reab.delete()
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
            rut=data['rut'],
            telefono=data.get('telefono', ''),
            correo=data.get('correo', '')
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
