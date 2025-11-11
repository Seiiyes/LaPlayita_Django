from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'correo', 'telefono', 'fecha_registro')
    search_fields = ('nombres', 'apellidos', 'correo', 'telefono')
    list_filter = ('fecha_registro',)
    ordering = ('-fecha_registro',)
