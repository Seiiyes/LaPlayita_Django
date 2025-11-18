app_name = 'reportes'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_reportes, name='panel_reportes'),
]
