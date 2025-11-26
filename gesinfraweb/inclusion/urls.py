# inclusion/urls.py
from django.urls import path
from . import views

app_name = 'inclusion'

urlpatterns = [
    path('', views.encuesta_inclusion, name='encuesta_inclusion'),
    path('resultados/<int:encuesta_id>/', views.resultados_encuesta, name='resultados_encuesta'),
]