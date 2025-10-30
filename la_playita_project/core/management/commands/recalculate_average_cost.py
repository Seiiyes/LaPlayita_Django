from django.core.management.base import BaseCommand
from core.models import Producto

class Command(BaseCommand):
    help = 'Recalculates the weighted average cost for all products.'

    def handle(self, *args, **options):
        self.stdout.write('Starting recalculation of average costs...')
        
        productos = Producto.objects.all()
        updated_count = 0

        for producto in productos:
            producto.actualizar_costo_promedio_y_stock()
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f'Updated {producto.nombre}'))

        self.stdout.write(self.style.SUCCESS(f'Finished. {updated_count} products were updated.'))
