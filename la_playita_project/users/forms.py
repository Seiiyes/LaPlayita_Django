from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Usuario, Rol

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
        # Asignar rol 'Vendedor' por defecto al registrarse
        user.rol = Rol.objects.get(nombre='Vendedor')
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset."""
        return Usuario.objects.filter(
            email__iexact=email,
            estado='activo',
        )