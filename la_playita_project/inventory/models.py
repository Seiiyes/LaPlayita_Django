from django.db import models
from django.db.models import Sum, F, DecimalField
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True


class Producto(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    costo_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Costo promedio ponderado, calculado automáticamente.")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    stock_minimo = models.PositiveIntegerField(default=10)
    stock_actual = models.PositiveIntegerField(default=0, help_text="Calculado automáticamente a partir de los lotes.")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.nombre

    def actualizar_costo_promedio_y_stock(self):
        lotes = self.lote_set.all()
        aggregates = lotes.aggregate(
            total_stock=Sum('cantidad_disponible'),
            total_cost=Sum(F('cantidad_disponible') * F('costo_unitario_lote'), output_field=DecimalField())
        )
        new_stock = aggregates['total_stock'] or 0
        total_cost = aggregates['total_cost'] or 0
        self.stock_actual = new_stock
        self.costo_promedio = total_cost / new_stock if new_stock > 0 else 0
        self.save(update_fields=['stock_actual', 'costo_promedio'])

    class Meta:
        managed = True


class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    reabastecimiento_detalle = models.ForeignKey('suppliers.ReabastecimientoDetalle', on_delete=models.SET_NULL, null=True, blank=True)
    numero_lote = models.CharField(max_length=50)
    cantidad_disponible = models.PositiveIntegerField()
    costo_unitario_lote = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_caducidad = models.DateField()
    fecha_entrada = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Lote {self.numero_lote} ({self.producto.nombre})"

    class Meta:
        managed = True
        unique_together = (('producto', 'numero_lote'),)


class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    lote = models.ForeignKey(Lote, models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField()
    tipo_movimiento = models.CharField(max_length=20)
    fecha_movimiento = models.DateTimeField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True