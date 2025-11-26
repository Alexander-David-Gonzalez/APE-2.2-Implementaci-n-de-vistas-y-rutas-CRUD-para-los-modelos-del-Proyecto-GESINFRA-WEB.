# inclusion/admin.py
from django.contrib import admin
from .models import *

admin.site.register(EncuestaInclusion)
admin.site.register(PreguntaInclusion)
admin.site.register(RespuestaInclusion)
admin.site.register(Recomendacion)