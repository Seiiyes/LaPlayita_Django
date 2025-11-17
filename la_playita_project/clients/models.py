from django.db import models

class Cliente(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=25)
    puntos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        managed = False


class PuntosFidelizacion(models.Model):
    TIPO_GANANCIA = 'ganancia'
    TIPO_CANJE = 'canje'
    TIPO_AJUSTE = 'ajuste'
    
    TIPO_CHOICES = [
        (TIPO_GANANCIA, 'Ganancia por Compra'),
        (TIPO_CANJE, 'Canje de Producto'),
        (TIPO_AJUSTE, 'Ajuste Manual'),
    ]
    
    cliente_id = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    puntos = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255)
    venta_id = models.IntegerField(null=True, blank=True)
    canje_id = models.BigIntegerField(null=True, blank=True)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cliente {self.cliente_id} - {self.tipo} - {self.puntos} pts"
    
    class Meta:
        verbose_name = 'Transacción de Puntos'
        verbose_name_plural = 'Transacciones de Puntos'
        db_table = 'puntos_fidelizacion'
        managed = False
        ordering = ['-fecha_transaccion']


class ProductoCanjeble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    puntos_requeridos = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='canjeables/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.puntos_requeridos} pts)"
    
    class Meta:
        verbose_name = 'Producto Canjeble'
        verbose_name_plural = 'Productos Canjebles'
        db_table = 'producto_canjeble'
        managed = False


class CanjeProducto(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_COMPLETADO = 'completado'
    ESTADO_CANCELADO = 'cancelado'
    
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_COMPLETADO, 'Completado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]
    
    cliente_id = models.IntegerField()
    producto_id = models.BigIntegerField()
    puntos_gastados = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    fecha_canje = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Canje #{self.id} - Cliente {self.cliente_id}"
    
    class Meta:
        verbose_name = 'Canje de Producto'
        verbose_name_plural = 'Canjes de Productos'
        db_table = 'canje_producto'
        managed = False
        ordering = ['-fecha_canje']
