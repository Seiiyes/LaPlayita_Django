# C:\laplayita\la_playita_project\core\urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

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
    # Restablecimiento de Contraseña
    # ----------------------------------------------
    path('accounts/password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             form_class=CustomPasswordResetForm,
             html_email_template_name='registration/password_reset_html_email.html'
         ), 
         name='password_reset'),
    path('accounts/password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('accounts/reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),

# ----------------------------------------------
# Gestión de Inventario (Productos)
# ----------------------------------------------
    path('inventario/', views.inventario_list, name='inventario_list'),
    path('inventario/alertas/', views.alertas_stock_list, name='alertas_stock'),
    path('inventario/crear/', views.producto_create, name='producto_create'),
    path('inventario/ajax/crear/', views.producto_create_ajax, name='producto_create_ajax'),
    path('inventario/producto/<int:pk>/json/', views.producto_detail_json, name='producto_detail_json'),
    path('inventario/producto/<int:pk>/lotes/json/', views.producto_lotes_json, name='producto_lotes_json'),
    path('inventario/categoria/add/', views.categoria_create, name='categoria_create'),
    path('inventario/editar/<int:pk>/', views.producto_update, name='producto_update'),
    path('inventario/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('proveedores/crear/', views.proveedor_create_ajax, name='proveedor_create'),
    path('categorias/crear/', views.categoria_create_ajax, name='categoria_create_ajax'),
    path('clientes/crear/ajax/', views.cliente_create_ajax, name='cliente_create_ajax'),    # ----------------------------------------------
    # Gestión de Lotes (Trazabilidad)
    # ----------------------------------------------
    path('inventario/producto/<int:producto_pk>/lotes/', views.lote_list, name='lote_list'),
    path('inventario/producto/<int:producto_pk>/lotes/crear/', views.lote_create, name='lote_create'),
    path('inventario/producto/<int:producto_pk>/lotes/crear/form/', views.lote_create_form_ajax, name='lote_create_form_ajax'),
    path('lotes/editar/<int:pk>/', views.lote_update, name='lote_update'),
    path('lotes/eliminar/<int:pk>/', views.lote_delete, name='lote_delete'),

    # Se mantienen otras rutas por si son necesarias en el futuro, pero se pueden limpiar.
    path('venta/', views.pos_view, name='pos_view'),
    path('reportes/', views.reportes_home, name='reportes_home'),
    path('clientes/', views.cliente_list, name='cliente_list'),
    # Reabastecimiento
    path('reabastecimientos/', views.reabastecimiento_list, name='reabastecimiento_list'),
    path('reabastecimientos/crear/', views.reabastecimiento_create, name='reabastecimiento_create'),
    path('reabastecimientos/<int:pk>/editar/', views.reabastecimiento_editar, name='reabastecimiento_editar'),
    path('reabastecimientos/<int:pk>/actualizar/', views.reabastecimiento_update, name='reabastecimiento_update'),
    path('reabastecimientos/<int:pk>/eliminar/', views.reabastecimiento_eliminar, name='reabastecimiento_eliminar'),
    path('reabastecimientos/<int:pk>/recibir/', views.reabastecimiento_recibir, name='reabastecimiento_recibir'),
    path('ventas/procesar/', views.procesar_venta, name='procesar_venta'),

    # ----------------------------------------------
    # PQRS
    # ----------------------------------------------
    path('pqrs/', views.pqrs_list, name='pqrs_list'),

    path('pqrs/<int:pk>/', views.pqrs_detail, name='pqrs_detail'),
    path('pqrs/<int:pk>/update/', views.pqrs_update, name='pqrs_update'),
    path('pqrs/<int:pk>/eliminar/', views.pqrs_delete, name='pqrs_delete'),
]
