# C:\laplayita\la_playita_project\core\urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------------------------
    # Autenticación y Flujo de Roles
    # ----------------------------------------------
    path('', views.landing_view, name='landing'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.login_redirect_view, name='login_redirect'), # Redirige después del login

    # ----------------------------------------------
    # 1. Dashboard y Alertas (HU-004)
    # ----------------------------------------------
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('alertas/', views.alertas_stock, name='alertas_stock'),

    # ----------------------------------------------
    # 2. Gestión de Inventario (HU-003, RF-1, RF-2)
    # ----------------------------------------------
    path('inventario/', views.inventario_list, name='inventario_list'),
    path('inventario/producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('inventario/producto/nuevo/', views.producto_create, name='producto_create'),
    path('inventario/producto/<int:pk>/editar/', views.producto_update, name='producto_update'),
    
    # ----------------------------------------------
    # 3. Punto de Venta (POS) (HU-005, HU-006)
    # ----------------------------------------------
    path('venta/', views.pos_view, name='pos_view'), # Pantalla principal de registro de venta
    path('venta/registrar/', views.registrar_venta, name='registrar_venta'), # Endpoint para procesar la venta (RF-6)

    # ----------------------------------------------
    # 4. Reportes (HU-008, HU-002)
    # ----------------------------------------------
    path('reportes/', views.reportes_home, name='reportes_home'),
    path('reportes/ventas/', views.reporte_ventas_periodo, name='reporte_ventas_periodo'),
    path('reportes/pqrs/', views.reporte_pqrs, name='reporte_pqrs'), # Seguimiento PQRS (HU-002)
    
    # ----------------------------------------------
    # 5. Maestros
    # ----------------------------------------------
    path('clientes/', views.cliente_list, name='cliente_list'),
]
