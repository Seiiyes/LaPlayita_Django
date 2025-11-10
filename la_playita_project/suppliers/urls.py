from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    path('proveedor/crear_ajax/', views.proveedor_create_ajax, name='proveedor_create_ajax'),

    path('reabastecimientos/', views.reabastecimiento_list, name='reabastecimiento_list'),
    path('reabastecimientos/crear/', views.reabastecimiento_create, name='reabastecimiento_create'),
    path('reabastecimientos/<int:pk>/editar/', views.reabastecimiento_editar, name='reabastecimiento_editar'),
    path('reabastecimientos/<int:pk>/actualizar/', views.reabastecimiento_update, name='reabastecimiento_update'),
    path('reabastecimientos/<int:pk>/recibir/', views.reabastecimiento_recibir, name='reabastecimiento_recibir'),
    path('reabastecimientos/<int:pk>/eliminar/', views.reabastecimiento_eliminar, name='reabastecimiento_eliminar'),
    path('categoria/crear_ajax/', views.categoria_create_ajax, name='categoria_create_ajax'),
    path('producto/crear_ajax/', views.producto_create_ajax, name='producto_create_ajax'),
]