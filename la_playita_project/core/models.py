# C:\laplayita\la_playita_project\core\models.py (Contenido corregido)

# This is an auto-generated Django model module.
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'categoria'


class Cliente(models.Model):
    documento = models.CharField(unique=True, max_length=20)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.CharField(max_length=60)
    telefono = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.documento})"

    class Meta:
        managed = False
        db_table = 'cliente'


class Producto(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    stock_minimo = models.IntegerField()
    # Mantenemos DO_NOTHING para la Categoría para proteger los productos.
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING) 

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'producto'


class Lote(models.Model):
    # CORREGIDO: ON DELETE CASCADE, si se va el producto, se va el lote.
    producto = models.ForeignKey(Producto, models.CASCADE) 
    numero_lote = models.CharField(max_length=50)
    cantidad_disponible = models.PositiveIntegerField()
    costo_unitario_lote = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_caducidad = models.DateField()
    # Le quitamos el valor por defecto para que no interfiera con la DB existente
    fecha_entrada = models.DateTimeField() 

    def __str__(self):
        return f"Lote {self.numero_lote} ({self.producto.nombre})"

    class Meta:
        managed = False
        db_table = 'lote'
        unique_together = (('producto', 'numero_lote'),)


class Rol(models.Model):
    nombre = models.CharField(unique=True, max_length=35)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'rol'


class Usuario(models.Model):
    documento = models.CharField(unique=True, max_length=20)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.CharField(unique=True, max_length=60)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    contrasena = models.CharField(max_length=255)
    estado = models.CharField(max_length=20)
    # Le quitamos el valor por defecto para que no interfiera con la DB existente
    fecha_creacion = models.DateTimeField() 
    ultimo_login = models.DateTimeField(blank=True, null=True)
    # Mantenemos DO_NOTHING para proteger usuarios del borrado de roles.
    rol = models.ForeignKey(Rol, models.DO_NOTHING) 
    reset_token = models.CharField(max_length=36, blank=True, null=True)
    reset_token_expiracion = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.rol.nombre})"

    class Meta:
        managed = False
        db_table = 'usuario'


class Venta(models.Model):
    fecha_venta = models.DateTimeField()
    metodo_pago = models.CharField(max_length=25)
    canal_venta = models.CharField(max_length=20)
    # Mantenemos DO_NOTHING para proteger el historial de ventas.
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING) 
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'venta'


class VentaDetalle(models.Model):
    # CORREGIDO: ON DELETE CASCADE, si se elimina la Venta, se eliminan los detalles.
    venta = models.ForeignKey(Venta, models.CASCADE) 
    # Mantenemos DO_NOTHING para proteger la integridad de la venta histórica.
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    lote = models.ForeignKey(Lote, models.DO_NOTHING)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'venta_detalle'


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre_empresa

    class Meta:
        managed = False
        db_table = 'proveedor'


class Reabastecimiento(models.Model):
    fecha = models.DateTimeField()
    costo_total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, blank=True, null=True)
    forma_pago = models.CharField(max_length=25, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    # Mantenemos DO_NOTHING para proteger el registro de reabastecimiento.
    proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING) 

    class Meta:
        managed = False
        db_table = 'reabastecimiento'


class ReabastecimientoDetalle(models.Model):
    # CORREGIDO: Si el Reabastecimiento se elimina, sus detalles deben irse (CASCADE).
    reabastecimiento = models.ForeignKey(Reabastecimiento, models.CASCADE) 
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'reabastecimiento_detalle'


class MovimientoInventario(models.Model):
    # Mantenemos DO_NOTHING ya que los movimientos son registros históricos que deben persistir.
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    lote = models.ForeignKey(Lote, models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField()
    tipo_movimiento = models.CharField(max_length=20)
    fecha_movimiento = models.DateTimeField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    venta_id = models.IntegerField(blank=True, null=True)
    reabastecimiento_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimiento_inventario'


class Pqrs(models.Model):
    tipo = models.CharField(max_length=20)
    descripcion = models.TextField()
    respuesta = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)
    # Mantenemos DO_NOTHING.
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING) 
    # CORREGIDO: ON DELETE SET NULL para Usuario, si el usuario se elimina.
    usuario = models.ForeignKey(Usuario, models.SET_NULL, blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'pqrs'


class PqrsHistorial(models.Model):
    # CORREGIDO: ON DELETE CASCADE, si se elimina la PQRS, se elimina el Historial.
    pqrs = models.ForeignKey(Pqrs, models.CASCADE) 
    # CORREGIDO: ON DELETE SET NULL para Usuario.
    usuario = models.ForeignKey(Usuario, models.SET_NULL, blank=True, null=True) 
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    descripcion_cambio = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pqrs_historial'