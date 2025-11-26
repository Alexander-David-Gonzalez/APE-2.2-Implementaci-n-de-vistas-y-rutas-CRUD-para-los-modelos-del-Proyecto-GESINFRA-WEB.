# calificaciones/admin.py - VERSIÓN COMPLETA CORREGIDA
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html
from decimal import Decimal  # ← IMPORTACIÓN NECESARIA
from .models import *

class ActividadInline(admin.TabularInline):
    model = Actividad
    extra = 1
    fields = ['nombre', 'tipo', 'nota']

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'asignatura', 'trimestre', 'nota_formativa', 'nota_sumativa', 'nota_final', 'docente']
    list_filter = ['trimestre', 'asignatura', 'año_lectivo', 'docente']
    readonly_fields = ['docente', 'fecha_registro', 'calcular_notas_button']
    fieldsets = [
        ('Información Académica', {
            'fields': ['estudiante', 'asignatura', 'trimestre', 'año_lectivo', 'docente', 'fecha_registro']
        }),
        ('Notas Sumativas (30%)', {
            'fields': ['nota_examen', 'nota_proyecto']
        }),
        ('Resultados Calculados', {
            'fields': ['nota_formativa', 'nota_sumativa', 'nota_final', 'calcular_notas_button'],
            'classes': ['collapse']
        }),
    ]
    
    inlines = [ActividadInline]
    
    def calcular_notas_button(self, obj):
        if obj.pk:
            url = reverse('admin:calcular_notas', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}">🔄 Calcular Notas Automáticamente</a>'
                '<br><small>Calculará: Formativa (promedio actividades 70%) + Sumativa (examen/proyecto 30%)</small>',
                url
            )
        return "Guarde primero la calificación para calcular notas"
    calcular_notas_button.short_description = "Cálculo Automático"
    calcular_notas_button.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.docente = request.user
        super().save_model(request, obj, form, change)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/calcular-notas/', self.admin_site.admin_view(self.calcular_notas_view), name='calcular_notas'),
        ]
        return custom_urls + urls
    
    def calcular_notas_view(self, request, object_id):
        try:
            calificacion = Calificacion.objects.get(id=object_id)
            
            # Calcular nota formativa (promedio actividades - 70%)
            actividades = calificacion.actividades.all()
            if actividades:
                # Convertir a Decimal para evitar problemas de tipo
                suma_actividades = sum(act.nota for act in actividades)
                nota_formativa = Decimal(str(suma_actividades)) / Decimal(str(len(actividades)))
            else:
                nota_formativa = Decimal('0.0')
            
            # Calcular nota sumativa (promedio examen/proyecto - 30%)
            notas_validas = []
            if calificacion.nota_examen > 0:
                notas_validas.append(calificacion.nota_examen)
            if calificacion.nota_proyecto > 0:
                notas_validas.append(calificacion.nota_proyecto)
                
            if notas_validas:
                suma_sumativas = sum(notas_validas)
                nota_sumativa = Decimal(str(suma_sumativas)) / Decimal(str(len(notas_validas)))
            else:
                nota_sumativa = Decimal('0.0')
            
            # Calcular nota final - USAR Decimal EN LUGAR DE float
            nota_final = (nota_formativa * Decimal('0.7')) + (nota_sumativa * Decimal('0.3'))
            
            # Actualizar redondeando a 2 decimales
            calificacion.nota_formativa = nota_formativa.quantize(Decimal('0.01'))
            calificacion.nota_sumativa = nota_sumativa.quantize(Decimal('0.01'))
            calificacion.nota_final = nota_final.quantize(Decimal('0.01'))
            calificacion.save()
            
            messages.success(
                request, 
                f'✅ Notas calculadas exitosamente:',
                extra_tags='safe'
            )
            
        except Calificacion.DoesNotExist:
            messages.error(request, '❌ No se encontró la calificación')
        except Exception as e:
            messages.error(request, f'❌ Error al calcular notas: {str(e)}')
        
        return redirect(reverse('admin:calificaciones_calificacion_change', args=[object_id]))

# Registrar otros modelos
admin.site.register(Estudiante)
admin.site.register(Asignatura)
admin.site.register(Paralelo)
admin.site.register(Trimestre)
admin.site.register(AnioLectivo)