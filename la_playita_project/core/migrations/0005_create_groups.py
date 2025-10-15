from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='Admin')
    Group.objects.create(name='Cashier')
    Group.objects.create(name='Vendedor')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_usuariogroups_usuariouserpermissions_and_more'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]