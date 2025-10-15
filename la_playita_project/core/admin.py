# C:\laplayita\la_playita_project\core\admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Categoria, Cliente, Producto, Lote, 
    Venta, VentaDetalle, Proveedor, Reabastecimiento, 
    Pqrs, PqrsHistorial
)

# Custom Admin for the custom User Model
class UsuarioAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'estado')
    
    # Fields to search by
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Filters
    list_filter = ('rol', 'estado')
    
    # Customize the fieldsets to include custom fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Campos Personalizados', {'fields': ('telefono', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Personalizados', {'fields': ('telefono', 'rol')}),
    )
    filter_horizontal = ()

# Unregister the default User admin if it's registered, then register our custom one
# This is a safety measure
# admin.site.unregister(Usuario) # Not needed if it was never registered with the default
admin.site.register(Usuario, UsuarioAdmin)

# Register the other models (Rol is removed)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Lote)
admin.site.register(Venta)
admin.site.register(VentaDetalle)
admin.site.register(Proveedor)
admin.site.register(Reabastecimiento)
admin.site.register(Pqrs)
admin.site.register(PqrsHistorial)