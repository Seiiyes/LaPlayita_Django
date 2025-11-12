#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_playita_project.settings')
django.setup()

from clients.models import Cliente
import json

clientes = Cliente.objects.all().order_by('nombres')
print(f'Total de clientes: {clientes.count()}')
print()

clientes_data = []
for c in clientes:
    print(f'Cliente: {c.id} - {c.nombres} {c.apellidos}')
    clientes_data.append({
        'id': c.id,
        'nombre': f"{c.nombres} {c.apellidos}".strip()
    })

print()
print('JSON Response:')
print(json.dumps({'success': True, 'clientes': clientes_data, 'total': len(clientes_data)}, indent=2, ensure_ascii=False))
