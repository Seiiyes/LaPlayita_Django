from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Lote, Producto

@receiver([post_save, post_delete], sender=Lote)
def actualizar_stock_producto(sender, instance, **kwargs):
    """
    Updates the 'stock_actual' of a Producto whenever a related Lote is saved or deleted.
    """
    producto = instance.producto
    total_stock = Lote.objects.filter(producto=producto).aggregate(total=Sum('cantidad_disponible'))['total']
    producto.stock_actual = total_stock if total_stock is not None else 0
    producto.save(update_fields=['stock_actual'])
