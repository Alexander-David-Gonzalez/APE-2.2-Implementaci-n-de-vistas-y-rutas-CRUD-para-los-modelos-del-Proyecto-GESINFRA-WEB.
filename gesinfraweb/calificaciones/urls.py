# calificaciones/urls.py
from django.urls import path
from . import views

app_name = 'calificaciones'

urlpatterns = [
    path('', views.registro_calificaciones, name='registro_calificaciones'),
    path('<int:calificacion_id>/', views.detalle_calificacion, name='detalle_calificacion'),
    path('actividad/<int:actividad_id>/eliminar/', views.eliminar_actividad, name='eliminar_actividad'),
]