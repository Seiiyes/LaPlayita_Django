from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core import views as core_views
from users import views as users_views

urlpatterns = [
    # Core y Autenticación (rutas principales)
    path('', core_views.landing_view, name='landing'),
    path('dashboard/', core_views.dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),

    path('users/', include('users.urls', namespace='users')), # Incluimos las URLs de la app users

    # Incluir URLs de otras apps con sus namespaces
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('suppliers/', include('suppliers.urls', namespace='suppliers')),
    path('pos/', include('pos.urls', namespace='pos')),
    path('pqrs/', include('pqrs.urls', namespace='pqrs')),

    # Ruta para la página de reportes
    path('reportes/', core_views.reportes_home_view, name='reportes_home'),
]