from django.contrib import admin
from django.urls import path, include

# Importamos el módulo de URLs de autenticación para usar sus patrones
from django.contrib.auth import urls as auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --------------------------------------------------------------------------
    # CORRECCIÓN: Usamos la sintaxis de tupla (patrones, app_name) en include().
    # Esto resuelve el error ImproperlyConfigured y define el namespace 'auth'.
    # --------------------------------------------------------------------------
    path('accounts/', include((auth_urls.urlpatterns, 'auth'), namespace='auth')), 
    
    # Rutas de tu aplicación core
    path('', include('core.urls')), 
]
