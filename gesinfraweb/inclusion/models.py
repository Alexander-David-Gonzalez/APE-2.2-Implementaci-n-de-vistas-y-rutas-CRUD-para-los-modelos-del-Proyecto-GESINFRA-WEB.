# inclusion/models.py
from django.db import models

class PreguntaInclusion(models.Model):
    CATEGORIA_CHOICES = [
        ('barreras_fisicas', 'Barreras Físicas'),
        ('senalizacion', 'Señalización'),
        ('espacios_aprendizaje', 'Espacios de Aprendizaje'),
        ('recursos_tecnologicos', 'Recursos Tecnológicos'),
        ('politicas_practicas', 'Políticas y Prácticas'),
    ]
    
    texto = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    
    def __str__(self):
        return f"{self.categoria}: {self.texto[:50]}..."

class EncuestaInclusion(models.Model):
    fecha = models.DateField(auto_now_add=True)
    evaluador = models.CharField(max_length=100)
    puntuacion_total = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Encuesta {self.fecha} - {self.evaluador}"

class RespuestaInclusion(models.Model):
    VALOR_CHOICES = [
        (1, 'Deficiente'),
        (2, 'Regular'),
        (3, 'Bueno'),
        (4, 'Excelente'),
    ]
    
    encuesta = models.ForeignKey(EncuestaInclusion, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaInclusion, on_delete=models.CASCADE)
    valor = models.IntegerField(choices=VALOR_CHOICES)
    
    class Meta:
        unique_together = ['encuesta', 'pregunta']
    
    def __str__(self):
        return f"{self.pregunta.categoria}: {self.valor}"

class Recomendacion(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta Prioridad'),
        ('media', 'Media Prioridad'),
        ('baja', 'Baja Prioridad'),
    ]
    
    encuesta = models.ForeignKey(EncuestaInclusion, on_delete=models.CASCADE)
    texto = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    
    def __str__(self):
        return f"Recomendación {self.prioridad}: {self.texto[:50]}..."