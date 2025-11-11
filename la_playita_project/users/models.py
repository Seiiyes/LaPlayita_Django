from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class Rol(models.Model):
    nombre = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'rol'


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

    # En el dump SQL `usuario.rol_id` es NOT NULL, alineamos permitiendo no-nulo y protegiendo eliminaciones
    rol = models.ForeignKey('Rol', on_delete=models.PROTECT, null=False, db_column='rol_id')

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
        managed = False
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