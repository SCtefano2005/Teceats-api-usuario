from django.db import models
from restaurantes.models import Restaurante  # Importa el modelo Restaurante

class Plato(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    id_restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'plato'  # Nombre de la tabla en la base de datos (opcional)
