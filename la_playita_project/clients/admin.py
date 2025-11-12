from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'correo', 'telefono')
    search_fields = ('nombres', 'apellidos', 'correo', 'telefono')
    ordering = ('nombres',)
