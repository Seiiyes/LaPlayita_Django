# C:\laplayita\la_playita_project\core\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from datetime import date, timedelta
from django.db import models

from .models import Producto, Lote
from .forms import VendedorRegistrationForm, ProductoForm, LoteForm, CategoriaForm
from .decorators import check_user_role

# ----------------------------------------------
# Vistas de Autenticación y Flujo
# ----------------------------------------------

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
    return render(request, 'core/landing.html')

@login_required
def login_redirect_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.rol_id in [1, 2]: # Admin y Vendedor
            return redirect('dashboard')
    return redirect('auth_login')

def register_view(request):
    if request.method == 'POST':
        form = VendedorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('auth_login')
    else:
        form = VendedorRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# ----------------------------------------------
# Dashboard
# ----------------------------------------------

@login_required
@check_user_role(allowed_roles=[1, 2])
def dashboard_view(request):
    productos_count = Producto.objects.count()
    productos_bajos_stock = Producto.objects.filter(stock_actual__lt=models.F('stock_minimo')).count()
    context = {
        'total_productos': productos_count,
        'productos_bajos_stock': productos_bajos_stock,
    }
    return render(request, 'core/dashboard.html', context)

# ----------------------------------------------
# Vistas de Gestión de Productos
# ----------------------------------------------

@login_required
@check_user_role(allowed_roles=[1, 2])
def inventario_list(request):
    productos = Producto.objects.select_related('categoria').all()
    form = ProductoForm() # Formulario vacío para el modal
    categoria_form = CategoriaForm() # Formulario vacío para el modal de categorías
    context = {
        'productos': productos,
        'form': form,
        'categoria_form': categoria_form,
    }
    return render(request, 'core/inventario_list.html', context)

@login_required
@check_user_role(allowed_roles=[1, 2])
def alertas_stock_list(request):
    productos = Producto.objects.filter(stock_actual__lt=models.F('stock_minimo')).select_related('categoria')
    form = ProductoForm()
    context = {
        'productos': productos,
        'form': form,
        'alertas_stock': True,
    }
    return render(request, 'core/inventario_list.html', context)

@login_required
@require_POST
@check_user_role(allowed_roles=[1, 2])
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
@check_user_role(allowed_roles=[1, 2])
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

@login_required
@require_POST
@check_user_role(allowed_roles=[1]) # Solo Admin puede eliminar
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return redirect('inventario_list')

@login_required
@require_POST
@check_user_role(allowed_roles=[1, 2])
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

@login_required
@check_user_role(allowed_roles=[1]) # Solo Admin
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

@login_required
@require_POST
@check_user_role(allowed_roles=[1]) # Solo Admin
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

@login_required
@check_user_role(allowed_roles=[1]) # Solo Admin
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

@login_required
@require_POST
@check_user_role(allowed_roles=[1]) # Solo Admin
def lote_delete(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    producto_pk = lote.producto.pk
    lote.delete()
    messages.success(request, 'Lote eliminado exitosamente.')
    return redirect('lote_list', producto_pk=producto_pk)