# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_equipos, name='lista_equipos'),
    path('equipo/nuevo/', views.nuevo_equipo, name='nuevo_equipo'),
    path('equipo/<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('falla/nueva/', views.nueva_falla, name='nueva_falla'),
]