from django import template
from django.db.models import Sum, F

register = template.Library()

@register.filter
def calculate_total_pending_value(reabastecimiento):
    if reabastecimiento.estado != 'recibido':
        return 0

    total_pending = reabastecimiento.reabastecimientodetalle_set.filter(
        cantidad_recibida__lt=F('cantidad')
    ).aggregate(
        total=Sum((F('cantidad') - F('cantidad_recibida')) * F('costo_unitario'))
    )['total']
    
    return total_pending if total_pending is not None else 0
