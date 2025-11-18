app_name = 'reportes'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_reportes, name='panel_reportes'),
    path('ventas/', views.reporte_ventas, name='reporte_ventas'),  # <-- Nueva ruta
]
