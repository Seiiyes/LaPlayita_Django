from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from core import views as core_views # Importamos las vistas de core

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),
    path('register/', core_views.register, name='register'),
    # Aquí puedes añadir más URLs específicas de la app 'users' en el futuro
]