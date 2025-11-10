from django.contrib import admin
from .models import Producto, Categoria, Lote, MovimientoInventario

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'stock_actual', 'stock_minimo', 'precio_unitario', 'costo_promedio')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    readonly_fields = ('stock_actual', 'costo_promedio')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('numero_lote', 'producto', 'cantidad_disponible', 'costo_unitario_lote', 'fecha_caducidad')
    list_filter = ('producto__categoria', 'fecha_caducidad')
    search_fields = ('numero_lote', 'producto__nombre')
    autocomplete_fields = ['producto']