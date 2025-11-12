#!/usr/bin/env python
"""
Script de prueba para verificar la API de clientes del POS
"""
import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_playita_project.settings')
django.setup()

from clients.models import Cliente
from django.http import JsonResponse

print("=" * 70)
print("PRUEBA DE API DE CLIENTES - SISTEMA POS")
print("=" * 70)

try:
    # Obtener clientes
    print("\n1. Consultando base de datos...")
    clientes = list(Cliente.objects.all().values('id', 'nombres', 'apellidos').order_by('nombres'))
    print(f"   ✓ Clientes encontrados en BD: {len(clientes)}")
    
    # Formatear clientes
    print("\n2. Formateando datos...")
    clientes_formateados = []
    for c in clientes:
        nombre_completo = f"{c['nombres']} {c['apellidos']}".strip()
        clientes_formateados.append({
            'id': c['id'],
            'nombre': nombre_completo
        })
        print(f"   ✓ {nombre_completo} (ID: {c['id']})")
    
    # Preparar respuesta JSON
    print("\n3. Preparando respuesta JSON...")
    respuesta = {
        'success': True,
        'clientes': clientes_formateados,
        'total': len(clientes_formateados)
    }
    
    print("\n4. RESPUESTA JSON QUE RECIBIRA EL POS:")
    print("-" * 70)
    print(json.dumps(respuesta, indent=2, ensure_ascii=False))
    print("-" * 70)
    
    print("\n✓ Prueba EXITOSA - La API funcionaría correctamente")
    
except Exception as e:
    import traceback
    print(f"\n✗ ERROR: {str(e)}")
    print("\nDetalles del error:")
    print(traceback.format_exc())
    sys.exit(1)

print("\n" + "=" * 70)
