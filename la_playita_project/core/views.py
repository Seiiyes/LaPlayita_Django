# C:\laplayita\la_playita_project\core\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import (
    Producto, Categoria, Cliente, MovimientoInventario, 
    Venta, Pqrs 
)
from django.db.models import Sum, F 
from datetime import date
from django.db import models # Importar 'models' para F() en las consultas
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .decorators import group_required

# ----------------------------------------------
# Vistas de Autenticación y Flujo
# ----------------------------------------------

def landing_view(request):
    """Muestra la landing page a usuarios no autenticados."""
    if request.user.is_authenticated:
        return redirect('login_redirect')
    return render(request, 'core/landing.html')

@login_required
def login_redirect_view(request):
    """Redirige a los usuarios según su rol (grupo)."""
    if request.user.groups.filter(name='Admin').exists():
        return redirect('admin:index')
    elif request.user.groups.filter(name='Cashier').exists():
        return redirect('dashboard')
    else:
        # Por defecto, si no tiene un rol asignado, va al dashboard.
        # Opcional: podrías redirigirlo a una página de "espera de aprobación".
        return redirect('dashboard')

def register_view(request):
    """Maneja el registro de nuevos Vendedores."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                vendedor_group = Group.objects.get(name='Vendedor')
                user.groups.add(vendedor_group)
            except Group.DoesNotExist:
                # Este es un error de configuración del servidor.
                # El grupo 'Vendedor' debe existir.
                # Se podría loggear este error.
                pass
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


# ----------------------------------------------
# 1. Dashboard y Alertas (HU-001, HU-004)
# ----------------------------------------------

@group_required('Admin', 'Cashier')
def dashboard_view(request):
    """Muestra el Dashboard principal con métricas clave y el acceso a alertas."""
    
    # 1. Calcular productos con stock bajo (HU-004)
    productos_en_alerta_qs = Producto.objects.annotate(
        stock_actual=Sum('lote__cantidad_disponible')
    ).filter(stock_actual__lt=F('stock_minimo'))
    
    # 2. Calcular métricas clave
    try:
        ventas_hoy_data = Venta.objects.filter(fecha_venta__date=date.today()).aggregate(
            total_ingreso=Sum('ventadetalle__subtotal')
        )
        ingresos_hoy = ventas_hoy_data.get('total_ingreso') or 0
    except:
        ingresos_hoy = 0
    
    context = {
        'total_productos': Producto.objects.count(),
        'productos_bajos_stock': productos_en_alerta_qs.count(),
        'ingresos_hoy': ingresos_hoy, 
    }
    return render(request, 'core/dashboard.html', context)

@group_required('Admin', 'Cashier')
def alertas_stock(request):
    """Vista detallada de los productos con stock bajo (HU-004)."""
    productos_en_alerta = Producto.objects.annotate(
        stock_actual=Sum('lote__cantidad_disponible')
    ).filter(stock_actual__lt=F('stock_minimo'))
    
    return render(request, 'core/alertas_stock.html', {'productos': productos_en_alerta})


# ----------------------------------------------
# 2. Gestión de Inventario (HU-003, RF-1, RF-2)
# ----------------------------------------------

@group_required('Admin', 'Cashier')
def inventario_list(request):
    """Lista todos los productos agrupados por Categoría (HU-003)."""
    categorias = Categoria.objects.annotate(
        total_stock=Sum('producto__lote__cantidad_disponible')
    ).prefetch_related('producto_set').all()
    
    context = {
        'categorias': categorias
    }
    return render(request, 'core/inventario_list.html', context)

@group_required('Admin')

def producto_create(request):
    """Vista para crear un nuevo Producto (RF-1)."""
    # Lógica de Forms de Django
    if request.method == 'POST':
        # Código para guardar el nuevo producto...
        return redirect('inventario_list')
    return render(request, 'core/producto_form.html')

@group_required('Admin')
def producto_detalle(request, pk):
    """Vista para ver el detalle de un producto."""
    # Lógica para obtener y mostrar un producto
    return render(request, 'core/producto_detalle.html')

@group_required('Admin')
def producto_update(request, pk):
    """Vista para actualizar un producto."""
    # Lógica de Forms de Django
    if request.method == 'POST':
        # Código para actualizar el producto...
        return redirect('inventario_list')
    return render(request, 'core/producto_form.html')

def pos_view(request):
    """Vista para el punto de venta."""
    return render(request, 'core/pos.html')

def registrar_venta(request):
    """Endpoint para registrar una venta."""
    return redirect('pos_view')

def reportes_home(request):
    """Vista para la página principal de reportes."""
    return render(request, 'core/reportes_home.html')

def reporte_ventas_periodo(request):
    """Vista para el reporte de ventas por período."""
    return render(request, 'core/reporte_ventas.html')

def reporte_pqrs(request):
    """Vista para el reporte de PQRS."""
    return render(request, 'core/reporte_pqrs.html')

def cliente_list(request):
    """Vista para listar los clientes."""
    return render(request, 'core/cliente_list.html')

# ... (el resto de las vistas se pueden proteger de manera similar)
