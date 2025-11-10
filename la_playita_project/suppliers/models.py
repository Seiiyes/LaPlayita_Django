from django.db import models
from django.utils import timezone


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        managed = True
        db_table = 'proveedor'


class Reabastecimiento(models.Model):
    ESTADO_SOLICITADO = 'solicitado'
    ESTADO_RECIBIDO = 'recibido'
    ESTADO_CANCELADO = 'cancelado'

    ESTADO_CHOICES = [
        (ESTADO_SOLICITADO, 'Solicitado'),
        (ESTADO_RECIBIDO, 'Recibido'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    FORMA_PAGO_TRANSFERENCIA = 'transferencia'
    FORMA_PAGO_EFECTIVO = 'efectivo'
    FORMA_PAGO_CHEQUE = 'cheque'
    FORMA_PAGO_PSE = 'pse'
    FORMA_PAGO_TARJETA_CREDITO = 'tarjeta_credito'
    FORMA_PAGO_CONSIGNACION = 'consignacion'

    FORMA_PAGO_CHOICES = [
        (FORMA_PAGO_TRANSFERENCIA, 'Transferencia Bancaria'),
        (FORMA_PAGO_EFECTIVO, 'Efectivo'),
        (FORMA_PAGO_CHEQUE, 'Cheque'),
        (FORMA_PAGO_PSE, 'PSE'),
        (FORMA_PAGO_TARJETA_CREDITO, 'Tarjeta de Crédito'),
        (FORMA_PAGO_CONSIGNACION, 'Consignación Bancaria'),
    ]

    fecha = models.DateTimeField(default=timezone.now)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_SOLICITADO, blank=True, null=True)
    forma_pago = models.CharField(max_length=25, choices=FORMA_PAGO_CHOICES, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True)

    class Meta:
        managed = True
        db_table = 'reabastecimiento'


class ReabastecimientoDetalle(models.Model):
    reabastecimiento = models.ForeignKey(Reabastecimiento, models.CASCADE, null=True)
    producto = models.ForeignKey('inventory.Producto', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    cantidad_recibida = models.IntegerField(default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_caducidad = models.DateField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'reabastecimiento_detalle'