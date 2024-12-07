from cloudinary.models import CloudinaryField
from django.db import models
from usuarios.models import DueñoRestaurante

class Restaurante(models.Model):
    PENDIENTE = 'Pendiente'
    APROBADO = 'Aprobado'
    RECHAZADO = 'Rechazado'

    STATUS_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    ]

    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_cocina = models.CharField(max_length=100, blank=True, null=True)
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    id_dueno = models.ForeignKey(DueñoRestaurante, on_delete=models.CASCADE)
    delivery_dentro = models.BooleanField(default=False)
    imagen_url = CloudinaryField('imagen_url', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDIENTE
    )

    def __str__(self):
        return self.nombre
    

class Repartidor(models.Model):
    VEHICULO_CHOICES = [
        ('A pie', 'A pie'),
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
        ('Bicicleta', 'Bicicleta'),
    ]

    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    vehiculo = models.CharField(max_length=20, choices=VEHICULO_CHOICES)
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='repartidores')

    def __str__(self):
        return f"{self.nombre} - {self.vehiculo}"
