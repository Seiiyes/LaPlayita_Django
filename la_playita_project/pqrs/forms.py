from django import forms
from .models import Pqrs


class PqrsForm(forms.ModelForm):
    class Meta:
        model = Pqrs
        fields = ['tipo', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class PqrsUpdateForm(forms.ModelForm):
    descripcion_cambio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label="Observación del cambio de estado", required=False)

    class Meta:
        model = Pqrs
        fields = ['respuesta', 'estado']
        widgets = {
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }