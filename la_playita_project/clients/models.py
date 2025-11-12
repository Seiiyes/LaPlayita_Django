from django.db import models


class Cliente(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=25)
    # Nota: fecha_registro existe en la tabla SQL pero se maneja manualmente
    # fecha_registro = models.DateTimeField(db_column='fecha_registro', blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = 'cliente'
        managed = False
