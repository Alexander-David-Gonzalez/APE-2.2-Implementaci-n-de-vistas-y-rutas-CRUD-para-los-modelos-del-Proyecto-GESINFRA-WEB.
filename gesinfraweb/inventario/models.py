# inventario/models.py
from django.db import models

class Equipo(models.Model):
    TIPO_CHOICES = [
        ('computadora', 'Computadora'),
        ('laptop', 'Laptop'),
        ('tablet', 'Tablet'),
        ('proyector', 'Proyector'),
        ('impresora', 'Impresora'),
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('servidor', 'Servidor'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
        ('baja', 'De Baja'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_serie = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_ingreso = models.DateField()
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.tipo} {self.marca} {self.modelo}"

class Falla(models.Model):
    ESTADO_CHOICES = [
        ('reportada', 'Reportada'),
        ('en_reparacion', 'En Reparación'),
        ('resuelta', 'Resuelta'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_reporte = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='reportada')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)
    
    def __str__(self):
        return f"Falla en {self.equipo} - {self.estado}"

class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    ]
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha = models.DateField()
    descripcion = models.TextField()
    responsable = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.tipo} - {self.equipo}"

class Red(models.Model):
    TIPO_CHOICES = [
        ('lan', 'LAN'),
        ('wlan', 'WLAN'),
        ('wan', 'WAN'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    nombre_red = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    configuracion = models.TextField(blank=True)  # Configuración de red
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre_red