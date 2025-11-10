from django import template

register = template.Library()

@register.filter
def calculate_total_pending_value(reabastecimiento):
    """
    Calcula el valor total pendiente de un reabastecimiento.
    """
    total_pending = 0
    for detalle in reabastecimiento.reabastecimientodetalle_set.all():
        total_pending += (detalle.cantidad - detalle.cantidad_recibida) * detalle.costo_unitario
    return total_pending