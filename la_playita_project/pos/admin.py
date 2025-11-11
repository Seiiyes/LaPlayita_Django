from django.contrib import admin
from .models import Venta, VentaDetalle, Pedido, PedidoDetalle


class VentaDetalleInline(admin.TabularInline):
    """Inline admin para detalles de venta"""
    model = VentaDetalle
    extra = 1
    fields = ('producto', 'lote', 'cantidad', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    """Admin para ventas con detalles inline"""
    list_display = ('id', 'fecha_venta', 'cliente', 'usuario', 'metodo_pago', 'canal_venta', 'total_venta')
    list_filter = ('fecha_venta', 'metodo_pago', 'canal_venta', 'usuario')
    search_fields = ('id', 'cliente__nombre', 'usuario__username')
    readonly_fields = ('fecha_venta', 'total_venta')
    inlines = [VentaDetalleInline]
    fieldsets = (
        ('Información General', {
            'fields': ('fecha_venta', 'usuario', 'cliente')
        }),
        ('Detalles de Pago', {
            'fields': ('metodo_pago', 'canal_venta', 'total_venta')
        }),
    )
    date_hierarchy = 'fecha_venta'


@admin.register(VentaDetalle)
class VentaDetalleAdmin(admin.ModelAdmin):
    """Admin para detalles de venta"""
    list_display = ('venta', 'producto', 'lote', 'cantidad', 'subtotal')
    list_filter = ('venta__fecha_venta', 'producto')
    search_fields = ('venta__id', 'producto__nombre')
    readonly_fields = ('subtotal',)


class PedidoDetalleInline(admin.TabularInline):
    """Inline admin para detalles de pedido"""
    model = PedidoDetalle
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Admin para pedidos con detalles inline"""
    list_display = ('id', 'cliente', 'estado', 'fecha_creacion', 'fecha_entrega_estimada', 'usuario', 'total')
    list_filter = ('estado', 'fecha_creacion', 'usuario')
    search_fields = ('id', 'cliente__nombre', 'cliente__apellido')
    readonly_fields = ('fecha_creacion', 'total')
    inlines = [PedidoDetalleInline]
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente', 'usuario')
        }),
        ('Estados y Fechas', {
            'fields': ('estado', 'fecha_creacion', 'fecha_entrega_estimada')
        }),
        ('Detalles Financieros', {
            'fields': ('total',)
        }),
        ('Adicional', {
            'fields': ('observaciones', 'venta'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'fecha_creacion'
    actions = ['marcar_en_preparacion', 'marcar_listo', 'marcar_completado', 'marcar_cancelado']

    def marcar_en_preparacion(self, request, queryset):
        """Acción para marcar pedidos en preparación"""
        updated = queryset.update(estado=Pedido.ESTADO_EN_PREPARACION)
        self.message_user(request, f'{updated} pedido(s) marcado(s) como en preparación.')
    marcar_en_preparacion.short_description = "Marcar como En Preparación"

    def marcar_listo(self, request, queryset):
        """Acción para marcar pedidos listos para entrega"""
        updated = queryset.update(estado=Pedido.ESTADO_LISTO_PARA_ENTREGA)
        self.message_user(request, f'{updated} pedido(s) marcado(s) como listo para entrega.')
    marcar_listo.short_description = "Marcar como Listo para Entrega"

    def marcar_completado(self, request, queryset):
        """Acción para marcar pedidos completados"""
        updated = queryset.update(estado=Pedido.ESTADO_COMPLETADO)
        self.message_user(request, f'{updated} pedido(s) marcado(s) como completado(s).')
    marcar_completado.short_description = "Marcar como Completado"

    def marcar_cancelado(self, request, queryset):
        """Acción para marcar pedidos cancelados"""
        updated = queryset.update(estado=Pedido.ESTADO_CANCELADO)
        self.message_user(request, f'{updated} pedido(s) cancelado(s).')
    marcar_cancelado.short_description = "Marcar como Cancelado"


@admin.register(PedidoDetalle)
class PedidoDetalleAdmin(admin.ModelAdmin):
    """Admin para detalles de pedido"""
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('pedido__fecha_creacion', 'producto')
    search_fields = ('pedido__id', 'producto__nombre')
    readonly_fields = ('subtotal',)
