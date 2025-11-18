from django.shortcuts import render
from django.db.models import Sum
from pos.models import Venta
from django.utils.dateparse import parse_date
from django.http import HttpResponse
import csv
from datetime import date
from openpyxl import Workbook

def panel_reportes(request):
    return render(request, 'reportes/panel_reportes.html', {})

def reporte_ventas(request):
    # Obtener parámetros de fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar ventas por rango de fechas si se proporcionan
    ventas = Venta.objects.all()
    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__gte=parse_date(fecha_inicio))
    if fecha_fin:
        ventas = ventas.filter(fecha_venta__lte=parse_date(fecha_fin))

    # Ventas del día
    ventas_hoy = ventas.filter(fecha_venta__date=date.today())

    # Ordenar y calcular el total
    ventas = ventas.order_by('-fecha_venta')
    total_ventas = ventas.aggregate(total=Sum('total_venta'))['total'] or 0
    total_ventas_hoy = ventas_hoy.aggregate(total=Sum('total_venta'))['total'] or 0

    # Descargar como Excel si se solicita
    if 'descargar' in request.GET:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte de Ventas"

        # Encabezados
        ws.append(['ID', 'Fecha', 'Cliente', 'Total'])

        # Datos
        for venta in ventas:
            ws.append([venta.id, venta.fecha_venta.strftime('%d/%m/%Y %H:%M'), f"{venta.cliente.nombres} {venta.cliente.apellidos}", venta.total_venta])

        # Agregar total de ventas al final del archivo Excel
        ws.append([])  # Fila vacía
        ws.append(['', '', 'Total de Ventas', total_ventas])

        wb.save(response)
        return response

    # Descargar como CSV si se solicita
    if 'descargar_csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Fecha', 'Cliente', 'Total'])
        for venta in ventas:
            writer.writerow([venta.id, venta.fecha_venta, f"{venta.cliente.nombres} {venta.cliente.apellidos}", venta.total_venta])

        return response

    return render(request, 'reportes/reporte_ventas.html', {
        'ventas': ventas,
        'ventas_hoy': ventas_hoy,
        'total_ventas': total_ventas,
        'total_ventas_hoy': total_ventas_hoy,
    })
