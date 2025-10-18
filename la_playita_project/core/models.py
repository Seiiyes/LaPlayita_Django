# C:\laplayita\la_playita_project\core\models.py (Refactored)
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


# --- Custom User Model ---
class Usuario(AbstractUser):
    """
    Custom User model inheriting from AbstractUser, mapped to the existing 'usuario' table.
    """
    password = models.CharField(db_column='contrasena', max_length=255)
    username = models.CharField(
        db_column='documento',
        max_length=150,
        unique=True,
        help_text='Documento de identidad.'
    )
    first_name = models.CharField(db_column='nombres', max_length=50)
    last_name = models.CharField(db_column='apellidos', max_length=50)
    email = models.EmailField(db_column='correo', max_length=60, unique=True)
    date_joined = models.DateTimeField(db_column='fecha_creacion', default=timezone.now)
    last_login = models.DateTimeField(db_column='ultimo_login', blank=True, null=True)

    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, default='activo')

    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, db_column='rol_id')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set",
        related_query_name="usuario",
        through='UsuarioGroups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set",
        related_query_name="usuario",
        through='UsuarioUserPermissions',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    @property
    def is_active(self):
        return self.estado == 'activo'

    @is_active.setter
    def is_active(self, value):
        self.estado = 'activo' if value else 'inactivo'

    @property
    def is_staff(self):
        return self.is_active

    @is_staff.setter
    def is_staff(self, value):
        pass

    @property
    def is_superuser(self):
        return self.is_active and self.rol and self.rol.nombre == 'Administrador'

    @is_superuser.setter
    def is_superuser(self, value):
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        managed = True
        db_table = 'usuario'

class UsuarioGroups(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='user_id')
    group = models.ForeignKey(Group, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('usuario', 'group'),)

class UsuarioUserPermissions(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='user_id')
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('usuario', 'permission'),)

# --- Other Models ---
class Rol(models.Model):
    nombre = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'rol'

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

# --- Inventory Models ---
class Producto(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    stock_minimo = models.IntegerField()
    stock_actual = models.PositiveIntegerField(default=0, help_text="Calculado automáticamente a partir de los lotes.")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # This logic could be useful if we need to perform actions when the product is saved directly,
        # but stock calculation is handled by signals from Lote.
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'producto'

class Lote(models.Model):
    producto = models.ForeignKey(Producto, models.CASCADE, default=1)
    reabastecimiento_detalle = models.ForeignKey('ReabastecimientoDetalle', on_delete=models.SET_NULL, null=True, blank=True)
    numero_lote = models.CharField(max_length=50)
    cantidad_disponible = models.PositiveIntegerField()
    costo_unitario_lote = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_caducidad = models.DateField()
    fecha_entrada = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Lote {self.numero_lote} ({self.producto.nombre})"

    @property
    def proveedor(self):
        return self.reabastecimiento_detalle.reabastecimiento.proveedor

    class Meta:
        managed = True
        db_table = 'lote'
        unique_together = (('producto', 'numero_lote'),)


# --- Other Unmanaged Models ---
class Venta(models.Model):
    fecha_venta = models.DateTimeField()
    metodo_pago = models.CharField(max_length=25)
    canal_venta = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'venta'

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, models.CASCADE)
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    lote = models.ForeignKey(Lote, models.DO_NOTHING)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'venta_detalle'

class Reabastecimiento(models.Model):
    fecha = models.DateTimeField()
    costo_total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, blank=True, null=True)
    forma_pago = models.CharField(max_length=25, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'reabastecimiento'

class ReabastecimientoDetalle(models.Model):
    reabastecimiento = models.ForeignKey(Reabastecimiento, models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'reabastecimiento_detalle'

class MovimientoInventario(models.Model):
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
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pqrs'

class PqrsHistorial(models.Model):
    pqrs = models.ForeignKey(Pqrs, models.CASCADE)
    usuario = models.ForeignKey(Usuario, models.SET_NULL, blank=True, null=True)
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    descripcion_cambio = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pqrs_historial'
