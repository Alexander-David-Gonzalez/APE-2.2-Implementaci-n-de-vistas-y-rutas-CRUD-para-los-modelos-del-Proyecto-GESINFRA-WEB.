# inventario/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Equipo)
admin.site.register(Falla)
admin.site.register(Mantenimiento)
admin.site.register(Red)