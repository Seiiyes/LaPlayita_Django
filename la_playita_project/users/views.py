from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .forms import VendedorRegistrationForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Redirige al dashboard si el usuario ya está autenticado
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


@never_cache
@login_required
def login_redirect_view(request):
    # Esta vista simplemente redirige al dashboard, actuando como un 'profile' genérico.
    return redirect('dashboard')

def register_view(request):
    if request.method == 'POST':
        form = VendedorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = VendedorRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
