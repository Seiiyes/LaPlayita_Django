from django.shortcuts import render

def panel_reportes(request):
    return render(request, 'reportes/panel_reportes.html', {})
