from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from .models import Usuario, Rol, Producto, Lote, Categoria

class VendedorRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Documento"
        self.fields['first_name'].label = "Nombres"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['telefono'].label = "Teléfono"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Rol.objects.get(nombre='Vendedor')
        if commit:
            user.save()
        return user

class ProductoForm(forms.ModelForm):
    precio_unitario = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    stock_minimo = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'precio_unitario', 'descripcion', 'stock_minimo', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoteForm(forms.ModelForm):
    cantidad_disponible = forms.IntegerField(
        label="Cantidad",
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    costo_unitario = forms.DecimalField(
        label="Costo por Unidad",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Lote
        fields = [
            'producto', 'numero_lote', 'cantidad_disponible', 'costo_unitario', 
            'fecha_caducidad'
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'numero_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
