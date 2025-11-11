from django.db import models
from django.utils import timezone
from django.conf import settings


class Venta(models.Model):
    fecha_venta = models.DateTimeField(default=timezone.now)
    metodo_pago = models.CharField(max_length=25)
    canal_venta = models.CharField(max_length=20)
    cliente = models.ForeignKey('clients.Cliente', models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        managed = True
        db_table = 'venta'

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, models.CASCADE)
    producto = models.ForeignKey('inventory.Producto', models.DO_NOTHING)
    lote = models.ForeignKey('inventory.Lote', models.DO_NOTHING)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'venta_detalle'


# --- Pedidos Models ---
class Pedido(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_EN_PREPARACION = 'en_preparacion'
    ESTADO_LISTO_PARA_ENTREGA = 'listo_para_entrega'
    ESTADO_COMPLETADO = 'completado'
    ESTADO_CANCELADO = 'cancelado'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_EN_PREPARACION, 'En Preparación'),
        (ESTADO_LISTO_PARA_ENTREGA, 'Listo para Entrega'),
        (ESTADO_COMPLETADO, 'Completado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey('clients.Cliente', on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="Empleado que registra el pedido.")
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_entrega_estimada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True, null=True)
    venta = models.OneToOneField(Venta, on_delete=models.SET_NULL, null=True, blank=True, help_text="Venta generada al completar el pedido.")

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

    class Meta:
        managed = True
        db_table = 'pedido'

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('inventory.Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, help_text="Precio del producto al momento de crear el pedido.")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'pedido_detalle'