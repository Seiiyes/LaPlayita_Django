from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE inventory_producto "
                "ADD COLUMN IF NOT EXISTS categoria_id BIGINT NULL;"
                " UPDATE inventory_producto SET categoria_id = 1 WHERE categoria_id IS NULL;"
                ""
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
