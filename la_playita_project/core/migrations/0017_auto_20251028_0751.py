from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_venta_cliente_venta_total_venta_venta_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='total_venta',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=12),
        ),
    ]