from django.contrib import admin
from .models import Proveedor, Reabastecimiento, ReabastecimientoDetalle


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
	list_display = ('nombre_empresa', 'telefono', 'correo')
	search_fields = ('nombre_empresa', 'correo')


@admin.register(Reabastecimiento)
class ReabastecimientoAdmin(admin.ModelAdmin):
	list_display = ('id', 'proveedor', 'fecha', 'costo_total', 'estado')
	list_filter = ('estado', 'fecha')
	search_fields = ('proveedor__nombre_empresa',)


@admin.register(ReabastecimientoDetalle)
class ReabastecimientoDetalleAdmin(admin.ModelAdmin):
	list_display = ('reabastecimiento', 'producto', 'cantidad', 'cantidad_recibida', 'costo_unitario')
	search_fields = ('producto__nombre',)

