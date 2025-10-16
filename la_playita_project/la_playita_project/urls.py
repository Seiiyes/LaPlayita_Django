from django.contrib import admin
from django.urls import path, include

# Importamos el módulo de URLs de autenticación para usar sus patrones
from django.contrib.auth import urls as auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
]
