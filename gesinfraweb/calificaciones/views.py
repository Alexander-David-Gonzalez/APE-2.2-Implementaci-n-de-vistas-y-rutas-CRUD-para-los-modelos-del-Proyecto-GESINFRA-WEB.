# calificaciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CalificacionForm, ActividadForm

@login_required
def registro_calificaciones(request):
    """Vista principal para registro de calificaciones"""
    # Solo mostrar estudiantes del docente logueado (si hay filtros)
    calificaciones = Calificacion.objects.filter(docente=request.user)
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST, user=request.user)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.docente = request.user
            calificacion.save()
            messages.success(request, 'Calificación registrada exitosamente')
            return redirect('detalle_calificacion', calificacion_id=calificacion.id)
    else:
        form = CalificacionForm(user=request.user)
    
    return render(request, 'calificaciones/registro.html', {
        'form': form,
        'calificaciones': calificaciones
    })

@login_required
def detalle_calificacion(request, calificacion_id):
    """Vista para agregar actividades y notas sumativas"""
    calificacion = get_object_or_404(Calificacion, id=calificacion_id, docente=request.user)
    
    if request.method == 'POST':
        # Procesar actividades
        if 'agregar_actividad' in request.POST:
            actividad_form = ActividadForm(request.POST)
            if actividad_form.is_valid():
                actividad = actividad_form.save(commit=False)
                actividad.calificacion = calificacion
                actividad.save()
                calificacion.save()  # Recalcular notas
                messages.success(request, 'Actividad agregada exitosamente')
                return redirect('detalle_calificacion', calificacion_id=calificacion.id)
        
        # Procesar notas sumativas
        elif 'guardar_notas' in request.POST:
            calificacion.nota_examen = request.POST.get('nota_examen', 0)
            calificacion.nota_proyecto = request.POST.get('nota_proyecto', 0)
            calificacion.save()
            messages.success(request, 'Notas sumativas guardadas exitosamente')
            return redirect('detalle_calificacion', calificacion_id=calificacion.id)
    
    actividad_form = ActividadForm()
    
    return render(request, 'calificaciones/detalle.html', {
        'calificacion': calificacion,
        'actividad_form': actividad_form
    })

@login_required
def eliminar_actividad(request, actividad_id):
    """Eliminar una actividad"""
    actividad = get_object_or_404(Actividad, id=actividad_id, calificacion__docente=request.user)
    calificacion_id = actividad.calificacion.id
    actividad.delete()
    actividad.calificacion.save()  # Recalcular notas
    messages.success(request, 'Actividad eliminada exitosamente')
    return redirect('detalle_calificacion', calificacion_id=calificacion_id)