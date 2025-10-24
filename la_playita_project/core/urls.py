# C:\laplayita\la_playita_project\core\urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ----------------------------------------------
    # Autenticación y Flujo Principal
    # ----------------------------------------------
    path('', views.landing_view, name='landing'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.login_redirect_view, name='login_redirect'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

# ----------------------------------------------
# Gestión de Inventario (Productos)
# ----------------------------------------------
    path('inventario/', views.inventario_list, name='inventario_list'),
    path('inventario/alertas/', views.alertas_stock_list, name='alertas_stock'),
    path('inventario/crear/', views.producto_create, name='producto_create'),
    path('inventario/ajax/crear/', views.producto_create_ajax, name='producto_create_ajax'),
    path('inventario/categoria/add/', views.categoria_create, name='categoria_create'),
    path('inventario/editar/<int:pk>/', views.producto_update, name='producto_update'),
    path('inventario/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('proveedores/crear/', views.proveedor_create_ajax, name='proveedor_create'),
    path('categorias/crear/', views.categoria_create_ajax, name='categoria_create_ajax'),    # ----------------------------------------------
    # Gestión de Lotes (Trazabilidad)
    # ----------------------------------------------
    path('inventario/producto/<int:producto_pk>/lotes/', views.lote_list, name='lote_list'),
    path('inventario/producto/<int:producto_pk>/lotes/crear/', views.lote_create, name='lote_create'),
    path('lotes/editar/<int:pk>/', views.lote_update, name='lote_update'),
    path('lotes/eliminar/<int:pk>/', views.lote_delete, name='lote_delete'),

    # Se mantienen otras rutas por si son necesarias en el futuro, pero se pueden limpiar.
    # path('venta/', views.pos_view, name='pos_view'),
    path('reportes/', views.reportes_home, name='reportes_home'),
    path('clientes/', views.cliente_list, name='cliente_list'),
    # Reabastecimiento
    path('reabastecimientos/', views.reabastecimiento_list, name='reabastecimiento_list'),
    path('reabastecimientos/crear/', views.reabastecimiento_create, name='reabastecimiento_create'),
    path('reabastecimientos/<int:pk>/editar/', views.reabastecimiento_editar, name='reabastecimiento_editar'),
    path('reabastecimientos/<int:pk>/eliminar/', views.reabastecimiento_eliminar, name='reabastecimiento_eliminar'),
]
