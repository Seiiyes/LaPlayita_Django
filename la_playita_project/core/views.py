# C:\laplayita\la_playita_project\core\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.db import models

from django.contrib.auth.decorators import login_required
from users.decorators import check_user_role
from inventory.models import Producto
from suppliers.models import Proveedor, Reabastecimiento

def landing_view(request):
    """Vista de la página de inicio."""
    return render(request, 'core/landing.html')


@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def dashboard_view(request):
    productos_count = Producto.objects.count()
    productos_bajos_stock = Producto.objects.filter(stock_actual__lt=models.F('stock_minimo')).count()

    # Contadores útiles para el dashboard
    reabastecimientos_count = Reabastecimiento.objects.count()
    proveedores_count = Proveedor.objects.count()

    context = {
        'total_productos': productos_count,
        'productos_bajos_stock': productos_bajos_stock,
        'reabastecimientos_count': reabastecimientos_count,
        'proveedores_count': proveedores_count,
    }
    return render(request, 'core/dashboard.html', context)


@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def register(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    return render(request, 'core/placeholder.html')

@never_cache
@login_required
@check_user_role(allowed_roles=['Administrador'])
def reportes_home_view(request):
    """
    Vista de marcador de posición para la página de reportes.
    """
    return render(request, 'core/placeholder.html')
