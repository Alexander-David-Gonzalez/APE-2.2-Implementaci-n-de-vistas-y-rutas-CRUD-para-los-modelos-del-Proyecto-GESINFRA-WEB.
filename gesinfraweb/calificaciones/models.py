# calificaciones/models.py
from django.db import models
from django.contrib.auth.models import User

class Paralelo(models.Model):
    grado = models.IntegerField()
    nombre = models.CharField(max_length=1)
    
    def __str__(self):
        return f"{self.grado}° - Paralelo {self.nombre}"

class AnioLectivo(models.Model):
    periodo_academico = models.CharField(max_length=20)
    
    def __str__(self):
        return self.periodo_academico

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(blank=True)
    paralelo = models.ForeignKey(Paralelo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Trimestre(models.Model):
    numero = models.CharField(max_length=1, choices=[('1','1'),('2','2'),('3','3')])
    
    def __str__(self):
        return f"Trimestre {self.numero}"



class Calificacion(models.Model):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)
    trimestre = models.ForeignKey('Trimestre', on_delete=models.CASCADE)
    año_lectivo = models.ForeignKey('AnioLectivo', on_delete=models.CASCADE)
    docente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Notas sumativas (30%)
    nota_examen = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    nota_proyecto = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
    # Campos calculados - LOS MANTENEMOS PERO SIN CÁLCULO AUTOMÁTICO
    nota_formativa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    nota_sumativa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['estudiante', 'asignatura', 'trimestre', 'año_lectivo']
    
    # ELIMINAMOS el método calcular_notas() y save() personalizado
    # Para evitar el error del primary key
    
    def __str__(self):
        return f"{self.estudiante} - {self.asignatura} - T{self.trimestre.numero}"

class Actividad(models.Model):
    TIPO_CHOICES = [
        ('trabajo_grupal', 'Trabajo Grupal'),
        ('tarea_individual', 'Tarea Individual'),
        ('proyecto_aula', 'Proyecto de Aula'),
        ('exposicion', 'Exposición'),
        ('investigacion', 'Investigación'),
        ('practica_laboratorio', 'Práctica de Laboratorio'),
        ('ejercicios_clase', 'Ejercicios en Clase'),
        ('portafolio', 'Portafolio Estudiantil'),
        ('personalizada', 'Personalizada'),
    ]
    
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE, related_name='actividades')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='personalizada')
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # ELIMINAMOS save() y delete() personalizados para evitar problemas
    
    def __str__(self):
        return f"{self.nombre} - {self.nota}"