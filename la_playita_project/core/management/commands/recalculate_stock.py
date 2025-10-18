from django.core.management.base import BaseCommand
from django.db.models import Sum
from core.models import Producto, Lote

class Command(BaseCommand):
    help = 'Recalculates the stock for all products based on their lots.'

    def handle(self, *args, **options):
        self.stdout.write('Starting stock recalculation...')
        productos = Producto.objects.all()
        for producto in productos:
            total_stock = Lote.objects.filter(producto=producto).aggregate(total=Sum('cantidad_disponible'))['total']
            producto.stock_actual = total_stock if total_stock is not None else 0
            producto.save(update_fields=['stock_actual'])
        self.stdout.write(self.style.SUCCESS('Stock recalculation finished successfully.'))
