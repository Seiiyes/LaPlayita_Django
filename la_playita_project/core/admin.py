# C:\laplayita\la_playita_project\core\admin.py

from django.contrib import admin
from .models import (
    Categoria, Cliente, Producto, Lote, Rol, Usuario, 
    Venta, VentaDetalle, Proveedor, Reabastecimiento, 
    Pqrs, PqrsHistorial
)

admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Lote)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Venta)
admin.site.register(VentaDetalle)
admin.site.register(Proveedor)
admin.site.register(Reabastecimiento)
admin.site.register(Pqrs)
admin.site.register(PqrsHistorial)